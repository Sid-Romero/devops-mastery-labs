"""
Web Scraper Module for DevOps Content
=====================================
Fetches trending DevOps topics from multiple sources:
- Dev.to RSS feed
- Medium (DevOps tags)
- GitHub Trending repos
- CNCF Blog
- Reddit r/devops, r/kubernetes
- Hacker News (filtered for DevOps)
"""

import random
import requests
import feedparser
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from dataclasses import dataclass
from tenacity import retry, stop_after_attempt, wait_exponential
import re


@dataclass
class DevOpsTopic:
    """Represents a scraped DevOps topic"""
    title: str
    summary: str
    source: str
    url: str
    tags: List[str]
    technology: Optional[str] = None  # docker, kubernetes, helm, argocd, ansible


# Keywords to identify technology focus
TECH_KEYWORDS = {
    'docker': ['docker', 'container', 'dockerfile', 'compose', 'containerization', 'image', 'registry'],
    'kubernetes': ['kubernetes', 'k8s', 'kubectl', 'pod', 'deployment', 'service', 'ingress', 'cluster'],
    'helm': ['helm', 'chart', 'helmfile', 'helm chart', 'package manager'],
    'argocd': ['argocd', 'argo cd', 'argo-cd', 'gitops', 'argo', 'continuous delivery'],
    'ansible': ['ansible', 'playbook', 'inventory', 'ansible-playbook', 'automation', 'configuration management'],
}


def detect_technology(text: str) -> Optional[str]:
    """Detect which DevOps technology is mentioned in the text"""
    text_lower = text.lower()
    scores = {}

    for tech, keywords in TECH_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        if score > 0:
            scores[tech] = score

    if scores:
        return max(scores, key=scores.get)
    return None


class DevOpsScraper:
    """Main scraper class that aggregates content from multiple sources"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; DevOpsLabBot/1.0; +https://github.com/Sid-Romero/docker-mastery-labs)'
        }
        self.topics: List[DevOpsTopic] = []

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def _fetch_url(self, url: str) -> requests.Response:
        """Fetch URL with retry logic"""
        response = requests.get(url, headers=self.headers, timeout=15)
        response.raise_for_status()
        return response

    def scrape_devto(self) -> List[DevOpsTopic]:
        """Scrape Dev.to for DevOps articles"""
        topics = []
        tags = ['devops', 'docker', 'kubernetes', 'cloud', 'cicd', 'infrastructure']

        for tag in tags:
            try:
                url = f"https://dev.to/feed/tag/{tag}"
                feed = feedparser.parse(url)

                for entry in feed.entries[:5]:  # Top 5 per tag
                    tech = detect_technology(entry.title + ' ' + entry.get('summary', ''))
                    topics.append(DevOpsTopic(
                        title=entry.title,
                        summary=entry.get('summary', '')[:500],
                        source='dev.to',
                        url=entry.link,
                        tags=[tag],
                        technology=tech
                    ))
            except Exception as e:
                print(f"⚠️ Error scraping dev.to/{tag}: {e}")

        return topics

    def scrape_github_trending(self) -> List[DevOpsTopic]:
        """Scrape GitHub trending repos for DevOps-related projects"""
        topics = []
        languages = ['', 'go', 'python', 'shell']

        for lang in languages:
            try:
                url = f"https://github.com/trending/{lang}?since=weekly"
                response = self._fetch_url(url)
                soup = BeautifulSoup(response.text, 'lxml')

                # Find repo articles
                articles = soup.select('article.Box-row')[:10]

                for article in articles:
                    # Get repo name
                    h2 = article.select_one('h2 a')
                    if not h2:
                        continue

                    repo_name = h2.get_text(strip=True).replace('\n', '').replace(' ', '')
                    repo_url = 'https://github.com' + h2.get('href', '')

                    # Get description
                    desc_elem = article.select_one('p')
                    description = desc_elem.get_text(strip=True) if desc_elem else ''

                    # Check if DevOps-related
                    full_text = f"{repo_name} {description}".lower()
                    if any(kw in full_text for kws in TECH_KEYWORDS.values() for kw in kws):
                        tech = detect_technology(full_text)
                        topics.append(DevOpsTopic(
                            title=f"GitHub Trending: {repo_name}",
                            summary=description[:500],
                            source='github',
                            url=repo_url,
                            tags=['github', 'trending'],
                            technology=tech
                        ))
            except Exception as e:
                print(f"⚠️ Error scraping GitHub trending: {e}")

        return topics

    def scrape_cncf_blog(self) -> List[DevOpsTopic]:
        """Scrape CNCF blog for cloud-native content"""
        topics = []
        try:
            url = "https://www.cncf.io/blog/"
            response = self._fetch_url(url)
            soup = BeautifulSoup(response.text, 'lxml')

            articles = soup.select('article')[:10]

            for article in articles:
                title_elem = article.select_one('h3 a, h2 a, .entry-title a')
                if not title_elem:
                    continue

                title = title_elem.get_text(strip=True)
                link = title_elem.get('href', '')

                excerpt_elem = article.select_one('.entry-excerpt, .excerpt, p')
                excerpt = excerpt_elem.get_text(strip=True)[:500] if excerpt_elem else ''

                tech = detect_technology(title + ' ' + excerpt)
                topics.append(DevOpsTopic(
                    title=title,
                    summary=excerpt,
                    source='cncf',
                    url=link,
                    tags=['cncf', 'cloud-native'],
                    technology=tech
                ))
        except Exception as e:
            print(f"⚠️ Error scraping CNCF blog: {e}")

        return topics

    def scrape_reddit(self) -> List[DevOpsTopic]:
        """Scrape Reddit DevOps subreddits (public JSON API)"""
        topics = []
        subreddits = ['devops', 'kubernetes', 'docker', 'ansible']

        for sub in subreddits:
            try:
                url = f"https://www.reddit.com/r/{sub}/hot.json?limit=10"
                response = self._fetch_url(url)
                data = response.json()

                for post in data.get('data', {}).get('children', []):
                    post_data = post.get('data', {})
                    title = post_data.get('title', '')
                    selftext = post_data.get('selftext', '')[:500]
                    permalink = post_data.get('permalink', '')

                    # Skip non-relevant posts
                    if post_data.get('stickied') or not title:
                        continue

                    tech = detect_technology(title + ' ' + selftext)
                    topics.append(DevOpsTopic(
                        title=title,
                        summary=selftext,
                        source=f'reddit/r/{sub}',
                        url=f'https://reddit.com{permalink}',
                        tags=['reddit', sub],
                        technology=tech or sub
                    ))
            except Exception as e:
                print(f"⚠️ Error scraping Reddit r/{sub}: {e}")

        return topics

    def scrape_hackernews(self) -> List[DevOpsTopic]:
        """Scrape Hacker News for DevOps-related posts"""
        topics = []
        try:
            # Get top stories
            url = "https://hacker-news.firebaseio.com/v0/topstories.json"
            response = self._fetch_url(url)
            story_ids = response.json()[:50]  # Top 50

            for story_id in story_ids:
                try:
                    story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                    story_response = self._fetch_url(story_url)
                    story = story_response.json()

                    if not story or story.get('type') != 'story':
                        continue

                    title = story.get('title', '')
                    url = story.get('url', f"https://news.ycombinator.com/item?id={story_id}")

                    # Check if DevOps-related
                    if any(kw in title.lower() for kws in TECH_KEYWORDS.values() for kw in kws):
                        tech = detect_technology(title)
                        topics.append(DevOpsTopic(
                            title=title,
                            summary=f"Hacker News discussion with {story.get('score', 0)} points",
                            source='hackernews',
                            url=url,
                            tags=['hackernews'],
                            technology=tech
                        ))
                except Exception:
                    continue
        except Exception as e:
            print(f"⚠️ Error scraping Hacker News: {e}")

        return topics

    def scrape_medium(self) -> List[DevOpsTopic]:
        """Scrape Medium DevOps tags via RSS"""
        topics = []
        tags = ['devops', 'docker', 'kubernetes', 'cloud-computing']

        for tag in tags:
            try:
                url = f"https://medium.com/feed/tag/{tag}"
                feed = feedparser.parse(url)

                for entry in feed.entries[:5]:
                    # Clean HTML from summary
                    summary = BeautifulSoup(entry.get('summary', ''), 'lxml').get_text()[:500]

                    tech = detect_technology(entry.title + ' ' + summary)
                    topics.append(DevOpsTopic(
                        title=entry.title,
                        summary=summary,
                        source='medium',
                        url=entry.link,
                        tags=['medium', tag],
                        technology=tech
                    ))
            except Exception as e:
                print(f"⚠️ Error scraping Medium/{tag}: {e}")

        return topics

    def scrape_all(self) -> List[DevOpsTopic]:
        """Scrape all sources and aggregate topics"""
        print("Scraping DevOps content from multiple sources...")

        all_topics = []

        print(" Scraping Dev.to...")
        all_topics.extend(self.scrape_devto())

        print(" Scraping GitHub Trending...")
        all_topics.extend(self.scrape_github_trending())

        print(" Scraping CNCF Blog...")
        all_topics.extend(self.scrape_cncf_blog())

        print("  Scraping Reddit...")
        all_topics.extend(self.scrape_reddit())

        print("  Scraping Hacker News...")
        all_topics.extend(self.scrape_hackernews())

        print("  Scraping Medium...")
        all_topics.extend(self.scrape_medium())

        # Remove duplicates (by title similarity)
        seen_titles = set()
        unique_topics = []
        for topic in all_topics:
            # Simple dedup by normalized title
            normalized = re.sub(r'[^a-z0-9]', '', topic.title.lower())[:50]
            if normalized not in seen_titles:
                seen_titles.add(normalized)
                unique_topics.append(topic)

        print(f"✅ Scraped {len(unique_topics)} unique topics")
        self.topics = unique_topics
        return unique_topics

    def get_random_topic(self, technology: Optional[str] = None) -> Optional[DevOpsTopic]:
        """Get a random topic, optionally filtered by technology"""
        if not self.topics:
            self.scrape_all()

        candidates = self.topics
        if technology:
            candidates = [t for t in self.topics if t.technology == technology]
            if not candidates:
                # Fallback to any topic and force the technology
                candidates = self.topics

        if candidates:
            return random.choice(candidates)
        return None


# Standalone test
if __name__ == "__main__":
    scraper = DevOpsScraper()
    topics = scraper.scrape_all()

    print("\nSample topics:")
    for topic in random.sample(topics, min(5, len(topics))):
        print(f"  [{topic.technology or 'general'}] {topic.title[:60]}...")
        print(f"    Source: {topic.source} | URL: {topic.url[:50]}...")
        print()
