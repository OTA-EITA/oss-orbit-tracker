"""Notification module for sending updates to Discord/Slack.

This module handles sending formatted notifications to various platforms
when the trend data collection is complete.
"""

import logging
import os
from typing import Any, Dict, List, Optional

import requests
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)


class Notifier:
    """Notifier for sending updates to Discord/Slack."""
    
    def __init__(
        self,
        discord_webhook_url: Optional[str] = None,
        slack_webhook_url: Optional[str] = None
    ):
        """Initialize notifier with webhook URLs.
        
        Args:
            discord_webhook_url: Discord webhook URL (optional)
            slack_webhook_url: Slack webhook URL (optional)
        """
        # Support both env var names for flexibility
        self.discord_webhook_url = (
            discord_webhook_url 
            or os.getenv("DISCORD_WEBHOOK_URL")
        )
        
        self.slack_webhook_url = (
            slack_webhook_url 
            or os.getenv("SLACK_WEBHOOK_URL_MONITORING_CLOUDS")  # GitHub Actions name
            or os.getenv("SLACK_WEBHOOK_URL")  # Local dev name
        )
        
        if self.discord_webhook_url:
            logger.info("Discord webhook configured")
        
        if self.slack_webhook_url:
            logger.info("Slack webhook configured")
        
        if not self.discord_webhook_url and not self.slack_webhook_url:
            logger.info("No notification webhooks configured (optional)")
    
    def send_discord_notification(
        self,
        trending: List[Dict[str, Any]],
        hn_stories: List[Dict[str, Any]],
        collected_at: str,
        success: bool = True,
        error_message: Optional[str] = None
    ) -> bool:
        """Send notification to Discord.
        
        Args:
            trending: List of trending repositories
            hn_stories: List of HackerNews stories
            collected_at: Collection timestamp
            success: Whether the collection was successful
            error_message: Error message if failed
            
        Returns:
            True if notification sent successfully
        """
        if not self.discord_webhook_url:
            logger.debug("Discord webhook not configured, skipping")
            return False
        
        try:
            # Build Discord embed
            embed = self._build_discord_embed(
                trending, 
                hn_stories, 
                collected_at,
                success,
                error_message
            )
            
            payload = {
                "embeds": [embed]
            }
            
            response = requests.post(
                self.discord_webhook_url,
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            
            logger.info("Discord notification sent successfully")
            return True
            
        except RequestException as e:
            logger.error(f"Failed to send Discord notification: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending Discord notification: {e}")
            return False
    
    def send_slack_notification(
        self,
        trending: List[Dict[str, Any]],
        hn_stories: List[Dict[str, Any]],
        collected_at: str,
        success: bool = True,
        error_message: Optional[str] = None
    ) -> bool:
        """Send notification to Slack.
        
        Args:
            trending: List of trending repositories
            hn_stories: List of HackerNews stories
            collected_at: Collection timestamp
            success: Whether the collection was successful
            error_message: Error message if failed
            
        Returns:
            True if notification sent successfully
        """
        if not self.slack_webhook_url:
            logger.debug("Slack webhook not configured, skipping")
            return False
        
        try:
            # Build Slack message
            payload = self._build_slack_payload(
                trending,
                hn_stories,
                collected_at,
                success,
                error_message
            )
            
            response = requests.post(
                self.slack_webhook_url,
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            
            logger.info("Slack notification sent successfully")
            return True
            
        except RequestException as e:
            logger.error(f"Failed to send Slack notification: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending Slack notification: {e}")
            return False
    
    def send_all_notifications(
        self,
        trending: List[Dict[str, Any]],
        hn_stories: List[Dict[str, Any]],
        collected_at: str,
        success: bool = True,
        error_message: Optional[str] = None
    ) -> Dict[str, bool]:
        """Send notifications to all configured platforms.
        
        Args:
            trending: List of trending repositories
            hn_stories: List of HackerNews stories
            collected_at: Collection timestamp
            success: Whether the collection was successful
            error_message: Error message if failed
            
        Returns:
            Dictionary with platform names and success status
        """
        results = {}
        
        if self.discord_webhook_url:
            results['discord'] = self.send_discord_notification(
                trending, hn_stories, collected_at, success, error_message
            )
        
        if self.slack_webhook_url:
            results['slack'] = self.send_slack_notification(
                trending, hn_stories, collected_at, success, error_message
            )
        
        return results
    
    def _build_discord_embed(
        self,
        trending: List[Dict[str, Any]],
        hn_stories: List[Dict[str, Any]],
        collected_at: str,
        success: bool,
        error_message: Optional[str]
    ) -> Dict[str, Any]:
        """Build Discord embed message.
        
        Args:
            trending: Trending repositories
            hn_stories: HackerNews stories
            collected_at: Collection timestamp
            success: Success status
            error_message: Error message if failed
            
        Returns:
            Discord embed dictionary
        """
        if not success:
            return {
                "title": "[FAILED] OSS Orbit Tracker - Collection Failed",
                "description": f"Error: {error_message}",
                "color": 0xFF0000,  # Red
                "timestamp": collected_at,
                "footer": {
                    "text": "OSS Orbit Tracker"
                }
            }
        
        # Success message
        description = f"**Collected Data:**\n"
        description += f"- GitHub Repositories: {len(trending)}\n"
        description += f"- HackerNews Stories: {len(hn_stories)}\n"
        description += f"- Updated: {collected_at}\n\n"
        
        # Top 5 repos
        if trending:
            description += "**Top 5 GitHub Repositories:**\n"
            for idx, repo in enumerate(trending[:5], 1):
                stars = f"{repo['stars']:,}"
                description += f"{idx}. [{repo['name']}]({repo['url']}) - Stars: {stars}\n"
        
        # Top 3 HN stories
        if hn_stories:
            description += "\n**Top 3 HackerNews Stories:**\n"
            for idx, story in enumerate(hn_stories[:3], 1):
                description += f"{idx}. [{story['title'][:50]}...]({story['hn_url']}) - Score: {story['score']}\n"
        
        return {
            "title": "[SUCCESS] OSS Orbit Tracker - Daily Update Complete",
            "description": description,
            "color": 0x00FF00,  # Green
            "timestamp": collected_at,
            "footer": {
                "text": "OSS Orbit Tracker"
            }
        }
    
    def _build_slack_payload(
        self,
        trending: List[Dict[str, Any]],
        hn_stories: List[Dict[str, Any]],
        collected_at: str,
        success: bool,
        error_message: Optional[str]
    ) -> Dict[str, Any]:
        """Build Slack message payload.
        
        Args:
            trending: Trending repositories
            hn_stories: HackerNews stories
            collected_at: Collection timestamp
            success: Success status
            error_message: Error message if failed
            
        Returns:
            Slack payload dictionary
        """
        if not success:
            return {
                "text": f"[FAILED] OSS Orbit Tracker - Collection Failed\n\nError: {error_message}",
                "attachments": [
                    {
                        "color": "danger",
                        "footer": "OSS Orbit Tracker",
                        "ts": collected_at
                    }
                ]
            }
        
        # Success message
        text = "[SUCCESS] *OSS Orbit Tracker - Daily Update Complete*\n\n"
        text += f"*Collected Data:*\n"
        text += f"- GitHub Repositories: {len(trending)}\n"
        text += f"- HackerNews Stories: {len(hn_stories)}\n"
        text += f"- Updated: {collected_at}\n"
        
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": text
                }
            }
        ]
        
        # Top 5 repos
        if trending:
            repo_text = "*Top 5 GitHub Repositories:*\n"
            for idx, repo in enumerate(trending[:5], 1):
                stars = f"{repo['stars']:,}"
                repo_text += f"{idx}. <{repo['url']}|{repo['name']}> - Stars: {stars}\n"
            
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": repo_text
                }
            })
        
        # Top 3 HN stories
        if hn_stories:
            hn_text = "*Top 3 HackerNews Stories:*\n"
            for idx, story in enumerate(hn_stories[:3], 1):
                hn_text += f"{idx}. <{story['hn_url']}|{story['title'][:50]}...> - Score: {story['score']}\n"
            
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": hn_text
                }
            })
        
        return {
            "text": "OSS Orbit Tracker Update",
            "blocks": blocks
        }
