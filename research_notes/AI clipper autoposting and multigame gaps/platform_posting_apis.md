# Platform posting and analytics API rules for GCM Clipper (as of 4 Nov 2026)

Research budget note: about 18 tool calls. Official docs were fetched for YouTube (quota page, videos.insert, revision history, Analytics dimensions) and Instagram (content publishing, media insights, user insights). Everything else comes from search summaries, mostly third-party or vendor pages. Those are marked as such.

## YouTube: posting, quota, the private-lock rule, scheduling, Shorts, analytics, OAuth verification

### Takeaway
YouTube changed a lot in 2025-2026. Uploads no longer cost 1,600 units. Since 1 June 2026, `videos.insert` costs 1 unit in its own bucket of 100 calls a day per project, separate from the 10,000-unit shared pool. On 2 November 2026, two days before this research, Google lifted the 2020 rule that kept uploads from unaudited API projects private. A small app can now auto-post public Shorts without passing the YouTube API audit first. The 100 uploads a day per project is the real ceiling for a multi-creator app.

### Cited Findings
- **Quota now:** "videos.insert: 1 unit per call, but it has its own bucket of 100 calls per day." `search.list` likewise costs 1 unit with its own bucket of 100 calls a day. The default daily quota of 10,000 units is shared across all other endpoints. Quotas reset at midnight Pacific Time. — [YouTube Data API quota costs](https://developers.google.com/youtube/v3/determine_quota_cost)
- **Other costs:** `videos.list` costs 1 unit, `videos.update` 50 units and `thumbnails.set` 50 units. — [YouTube quota costs](https://developers.google.com/youtube/v3/determine_quota_cost)
- **The videos.insert reference agrees:** each call uses 1 unit from the "Video Uploads" bucket, limited to 100 calls a day. The maximum file size is 256 GB. Accepted MIME types are `video/*` and `application/octet-stream`. — [videos.insert](https://developers.google.com/youtube/v3/docs/videos/insert)
- **Scopes for upload (any one of these):** `youtube.upload`, `youtube`, `youtubepartner`, `youtube.force-ssl`. — [videos.insert](https://developers.google.com/youtube/v3/docs/videos/insert)
- **How the cost changed, from the revision history:**
  - 4 Dec 2025: docs and the Quota Calculator were updated to "reflect a change in the quota cost of a video upload from approximately 1600 units to approximately 100 units."
  - 1 Jun 2026: "The YouTube Data API is transitioning to a granular quota system covering smaller sets of methods". `videos.insert` and `search.list` moved to their own buckets, and "API calls to all other methods will be charged to the existing quota bucket."
  - 3 Jun 2026: a new `videos.batchGetStats` method costs 1 unit in its own bucket (default 10,000 units a day).

  — [YouTube Data API revision history](https://developers.google.com/youtube/v3/revision_history)
- **Private lock lifted, 2 Nov 2026:** videos uploaded by unverified API projects "are no longer restricted to private viewing mode", which reverses the July 2020 policy. If no privacy status is set, "the uploaded video's privacy status defaults to `public`", though the creator's account settings may still make it private. The videos.insert page now says the same. — [Revision history](https://developers.google.com/youtube/v3/revision_history); [videos.insert](https://developers.google.com/youtube/v3/docs/videos/insert)
- **Other 2026 changes:**
  - 3 Nov 2026: custom thumbnails can be uploaded for Shorts after processing finishes.
  - 14 Sep 2026: the thumbnail file size limit rose from 2 MB to 50 MB.
  - 27 Aug 2026: public views count the moment a video starts playing, aligned across long-form, Live and Shorts. Monetization still uses engaged views.
  - 7 Jul 2026: a new `brandPartner` part is settable on insert and update.
  - 26 Mar 2025 (effective 31 Mar 2025): a Shorts view counts every start or replay, with no minimum watch time.

  — [Revision history](https://developers.google.com/youtube/v3/revision_history)
- **Scheduling:** `status.publishAt` can be set on insert, and there is an `invalidPublishAt` 400 error. The page gives no other requirements. — [videos.insert](https://developers.google.com/youtube/v3/docs/videos/insert)
- **Shorts in the API:** the videos.insert page does not mention Shorts and has no "isShort" flag. — [videos.insert](https://developers.google.com/youtube/v3/docs/videos/insert)
- **Third-party sources lag:** some still list the old 1,600 or 100-unit costs against the shared pool, while others give 1 unit with 100 uploads a day. The official quota page above settles it. — [Phyllo](https://www.getphyllo.com/post/is-the-youtube-api-free-in-2026-quota-limits-costs-when-to-pay), [bundle.social, Aug 2026](https://bundle.social/blog/youtube-api-quota-exceeded-limits-fixes), [ChannelCrawler, Mar 2026](https://channelcrawler.com/insights/youtube-api-daily-limit-quotas-costs-and-how-to-scale-beyond-10000-units-channelcrawler)
- **Analytics, traffic source:** `insightTrafficSourceType` has a `SHORTS` value: "The viewer was referred by swiping vertically from the previous video in the Shorts viewing experience." — [YouTube Analytics dimensions](https://developers.google.com/youtube/analytics/dimensions)
- **Analytics, content type:** `creatorContentType` takes `SHORTS`, `LIVE_STREAM`, `STORY`, `VIDEO_ON_DEMAND` and `UNSPECIFIED`, with data from 1 Jan 2019. A Shorts clip's views can therefore be split from the source livestream's views. — [YouTube Analytics dimensions](https://developers.google.com/youtube/analytics/dimensions)
- **Analytics, retention:** with `elapsedVideoTimeRatio`, "The API returns 100 data points for each video with ratio values ranging from 0.01 to 1.0." — [YouTube Analytics dimensions](https://developers.google.com/youtube/analytics/dimensions)
- **Analytics, time dimensions:** only `day` and `month` exist, and dates run on Pacific time. There is no hour-of-day dimension. `livestreamPosition` gives minute-by-minute data inside a live stream, which may help when picking clips. The Reporting API equivalents are `traffic_source_type` and `elapsed_video_time_percentage`. — [YouTube Analytics dimensions](https://developers.google.com/youtube/analytics/dimensions); [Analytics vs Reporting mapping](https://developers.google.com/youtube/analytics/dimsmets/dims)
- **OAuth verification:** YouTube user-data scopes, `youtube.upload` among them, are classed as *sensitive*, not restricted, so the CASA security assessment does not normally apply. Google's sensitive-scope review "typically takes 3-5 business days" and needs a demo video and a justification for each scope. Third-party guides say incomplete justifications are the most common reason for rejection. — [Google sensitive scope verification](https://developers.google.com/identity/protocols/oauth2/production-readiness/sensitive-scope-verification); [Phyllo YouTube scopes](https://www.getphyllo.com/post/youtube-oauth-scopes); [singhamandeep.com (third party)](https://singhamandeep.com/?p=1402)
- **CASA for restricted scopes:** one guide says restricted scopes such as `youtubepartner` need a CASA Tier 2 assessment. This is from a third-party source and was not verified on Google's site. — [singhamandeep.com](https://singhamandeep.com/category/google-youtube-api/)

### Inferences
- The upload ceiling is per API project, not per creator. 100 uploads a day caps the whole app, for example about 33 creators at 3 Shorts a day each. More needs the YouTube API Services "Audit and Quota Extension" form, which still exists for quota increases. The form was not fetched this session, so its current review time is unverified.
- Use `youtube.upload` for posting and `yt-analytics.readonly` plus `youtube.readonly` for analytics. Avoid `youtubepartner` so the app stays in sensitive-scope verification and needs no CASA. While unverified, a Google OAuth app in "Testing" mode is limited to 100 test users and its refresh tokens expire after 7 days. That comes from general Google OAuth knowledge and was not re-verified here.
- The 2 Nov 2026 change happened two days ago. Watch for follow-up clarifications. Calling the API with `privacyStatus` set explicitly (private plus `publishAt` for scheduling) is safest.
- YouTube treats an upload as a Short from its shape and length (vertical or square and within the Shorts length limit), not from an API flag. The length limit rose from 60 seconds to 3 minutes in October 2024. That is from memory and was not re-verified this session, so it is a gap.
- With no hour dimension in the Analytics API, "best time to post" needs a proxy: daily views by publish hour across the creator's own past uploads. YouTube Studio's "When your viewers are on YouTube" heatmap does not appear among the documented API dimensions.

### Gaps
- Current review time for the YouTube quota-extension audit and whether it was changed in 2026. Not fetched.
- Shorts maximum length (believed to be 3 minutes) is not cited from an official 2026 source.
- Whether the Reporting API exposes any hour-level audience activity. Not confirmed.
- Whether the YouTube API Services Terms or Developer Policies changed alongside the 2 Nov 2026 unlock. Not checked.

## Instagram: Reels publishing, account types, permissions, limits, scheduling, insights, review

### Takeaway
Instagram can auto-publish Reels to professional (Business or Creator) accounts. With the newer "Instagram API with Instagram Login", the scopes are `instagram_business_basic` and `instagram_business_content_publish`, use `graph.instagram.com`, and need no Facebook Page in that flow. The limit is 100 API-published posts per 24 hours per account, though one section of the same page says 50. There is no native schedule parameter, so the app must hold posts and publish them at the chosen time. Reels insights now cover views, reach, saves, shares, reposts, average watch time, total watch time and skip rate. The public app needs Advanced Access through App Review plus Meta Business Verification.

### Cited Findings
- **Who can post:** content publishing works for Instagram professional accounts. — [Instagram content publishing](https://developers.facebook.com/docs/instagram-platform/content-publishing)
- **Three ways to log in:**
  - Instagram Login: `instagram_business_basic` and `instagram_business_content_publish`, with an Instagram User token on `graph.instagram.com`.
  - Facebook Login: `instagram_basic`, `instagram_content_publish` and `pages_read_engagement` (plus `ads_management` and `ads_read` if the user has a Business Manager role on the Page), with a Facebook Page token on `graph.facebook.com`.
  - Unified Login: a Business Integration System User token.

  The Facebook Login path needs a linked Facebook Page. If that Page requires Page Publishing Authorization, publishing is blocked until it is completed. — [Content publishing](https://developers.facebook.com/docs/instagram-platform/content-publishing)
- **Rate limit:** "100 API-published posts per 24-hour moving period". A carousel counts as one post. The carousel section of the same page gives a conflicting 50 per 24 hours. Usage can be checked at `GET /<IG_ID>/content_publishing_limit`. — [Content publishing](https://developers.facebook.com/docs/instagram-platform/content-publishing)
- **Publishing flow:**
  1. `POST /<IG_ID>/media` with `video_url`, or `upload_type=resumable` to upload to `rupload.facebook.com`, which supports a local file or a public URL.
  2. Poll the container's `status_code`, about once a minute for at most 5 minutes.
  3. `POST /<IG_ID>/media_publish` with the `creation_id`.

  Shopping tags and filters are not supported. — [Content publishing](https://developers.facebook.com/docs/instagram-platform/content-publishing)
- **Trial Reels:** supported through `trial_params.graduation_strategy` = `MANUAL` or `SS_PERFORMANCE`, which graduates the Reel automatically if it performs well. This could suit A/B testing clips with non-followers first. — [Content publishing](https://developers.facebook.com/docs/instagram-platform/content-publishing)
- **Scheduling:** no native scheduling parameter is documented. The guide says apps may let users schedule posts and must enforce the rate limit themselves. — [Content publishing](https://developers.facebook.com/docs/instagram-platform/content-publishing)
- **Reels media insights:**
  - Organic: `comments`, `likes`, `saved`, `shares`, `reposts`, `reach`, `views`, `total_interactions` (views and total_interactions are marked "in development").
  - Watch time and skips: `ig_reels_avg_watch_time`, `ig_reels_video_view_total_time` (in development), and `reels_skip_rate` (estimated; the share of views that skipped the first 3 seconds).
  - Cross-posting: `crossposted_views` and `facebook_views`.
  - Including ads (Facebook Login only): `total_views`, `total_likes`, `total_comments`.

  The Reels insights page does not list a "plays" metric. — [IG media insights](https://developers.facebook.com/docs/instagram-platform/reference/instagram-media/insights)
- **Insights permissions:** `instagram_business_manage_insights` with Instagram Login, or `instagram_manage_insights` plus `pages_read_engagement` with Facebook Login. Data can lag up to 48 hours and is kept for up to 2 years. — [IG media insights](https://developers.facebook.com/docs/instagram-platform/reference/instagram-media/insights)
- **Account insights:**
  - Metrics: `reach`, `views`, `follower_demographics` and `engaged_audience_demographics` (age, city, country, gender), plus interaction metrics (`saves`, `shares`, `reposts`, `profile_links_taps` and others).
  - 100-follower minimum: `follower_count`, `online_followers` and `follower_demographics` are not available under 100 followers.
  - `online_followers` (follower online times) data covers only the last 30 days.
  - `impressions` was deprecated on 21 Apr 2025 (v22.0 and all versions).

  — [IG user insights](https://developers.facebook.com/docs/instagram-platform/api-reference/instagram-user/insights)
- **App review and verification:** Advanced Access needs Meta App Review, and Business Verification is required for apps that need Advanced Access. An April 2026 Meta forum thread reports Business Verification stuck "In Review" for more than 10 days, which blocked App Review submission. That is one user's report, and no official timeline was found. — [Meta Instagram Platform overview](https://developers.facebook.com/docs/instagram-platform/overview); [Meta community forum, Apr 2026](https://communityforums.atmeta.com/questions-and-discussions-26/business-verification-in-review-10-days-blocking-app-review-submission-177498)
- **Existing approvals may carry over:** Meta docs say an existing app already approved for Advanced Access may be granted Instagram business permissions automatically. — [Create an Instagram app](https://developers.facebook.com/docs/instagram-platform/create-an-instagram-app)

### Inferences
- Use Instagram Login. Indian gaming creators usually have Creator accounts and often no Facebook Page, and this path avoids the Page requirement and its Publishing Authorization blocker.
- Business Verification needs a registered business identity: legal name, address and documents such as GST or Udyam. A solo developer may struggle before incorporating, which makes a unified posting API (see below) the faster route at launch.
- In Standard Access (before review), the app works only for accounts with a role on the app. That is fine for the owner's testing and a few beta creators added as testers. This is from general Meta platform knowledge and was not re-verified this session.

### Gaps
- Reels spec limits through the API (maximum length, file size, aspect ratio) were not given on the fetched page. The Reels-specific reference page was not fetched.
- Whether 100 or 50 posts a day applies; the official page contradicts itself.
- `share_to_feed` and audio or music handling for API-published Reels are not covered.
- No official App Review or Business Verification turnaround found.

## Facebook Pages Reels (brief)

### Takeaway
Not researched in depth this session. No cited facts.

### Cited Findings
- Facebook Login publishing for Instagram needs `pages_read_engagement` and a Page token, and Page Publishing Authorization can block publishing. — [Content publishing](https://developers.facebook.com/docs/instagram-platform/content-publishing)
- Instagram Reels insights include `crossposted_views` and `facebook_views` for Reels shared to Facebook. — [IG media insights](https://developers.facebook.com/docs/instagram-platform/reference/instagram-media/insights)

### Inferences
- Facebook Page Reels publishing exists through a Graph API `video_reels` flow using `pages_manage_posts` and related Page permissions. That is from prior knowledge and was not verified here. It needs the same Meta App Review and Business Verification as Instagram.

### Gaps
- Facebook Reels API endpoint details, per-Page daily limits and Reels insights metrics were not verified.

## TikTok: India status and Content Posting API audit

### Takeaway
TikTok is still banned in India: the June 2020 Section 69A order has not been lifted, and the government denied rumours of its return in early 2026. Its posting API matters only for non-India creators. Unaudited API clients post private only (SELF_ONLY), and the audit is said to take days to about 2 weeks.

### Cited Findings
- **Ban stands:** the government said no order has been issued to lift the ban and that reports of its return were false. A TikTok spokesperson said: "We have not restored access to TikTok in India." — [Patrika, Feb 2026](https://www.patrika.com/en/national-news/tiktok-ban-in-india-not-lifted-says-modi-government-19886142); [Storyboard18](https://www.storyboard18.com/amp/brand-makers/tiktok-ban-in-india-still-stands-company-clarifies-after-brief-website-access-79505.htm); [Business Standard](https://www.business-standard.com/india-news/tiktok-return-india-bytedance-job-openings-gurugram-office-125083100202_1.html)
- **Unconfirmed:** an Aug 2026 Patrika article discusses 36 banned Chinese apps returning. It is not clear whether TikTok is among them. — [Patrika, Aug 2026](https://www.patrika.com/latest-technology/36-banned-chinese-apps-return-to-india-tiktok-latest-update-19393479)
- **Unaudited clients:** "all content posted by unaudited clients will be restricted to private viewing mode". Publishing to a public account from an unaudited client fails with `unaudited_client_can_only_post_to_private_accounts`. Passing the audit lifts the restriction. — [TikTok Content Posting API reference](https://developers.tiktok.com/doc/content-posting-api-reference-photo-post)
- **Other unaudited limits:** up to 5 users can post in 24 hours, and their accounts must be private. — [Postiz docs](https://docs.postiz.com/self-host/providers/tiktok)
- **Audit timing:** the audit reviews the use case and a required posting UX and is said to take several days to two weeks. This is a secondary source. — [adaptlypost](https://adaptlypost.com/de/blog/why-does-my-app-need-approval-post-tiktok)

### Inferences
- Leave TikTok out of the India MVP. Add it later through a unified API that has already passed the audit, for non-India creators.

### Gaps
- Nothing confirmed newer than about Aug 2026 on the India ban.

## Indian short-video apps, X, Snapchat

### Takeaway
No public posting API was found for Moj, ShareChat or Josh, and no evidence of one for Chingari or MX TakaTak. X now runs a pay-per-use API from February 2026: about $0.015 per plain post and $0.20 per post containing a URL, from third-party sources. Snapchat Spotlight was not researched.

### Cited Findings
- No public developer upload API was found for Moj or ShareChat. The only developer tie-in found was a 2021 deal under which Moj uses Snap's Lens tools. — [Business Standard 2021](https://business-standard.com/amp/article/companies/sharechat-owned-video-app-moj-partners-with-snap-inc-for-snapchat-lenses-121021001037_1.html); [Moj on Product Hunt](https://www.producthunt.com/products/moj/makers)
- **X pricing:** pay-per-use launched in Feb 2026 at $0.01 per post created. In April 2026 a plain post went to $0.015 and a post with a URL to $0.20 (effective 20 Apr). Reads cost $0.005 a post and owned reads $0.001. Legacy Basic plans moved to pay-per-use after 1 Jun 2026. These are third-party sources citing X docs; X's official pricing page was not opened. — [opentweet.io](https://opentweet.io/x-api-pricing); [MediaNama, Feb 2026](https://www.medianama.com/2026/02/223-x-developer-api-pricing-pay-per-use-model/); [Upload-Post X pricing](https://www.upload-post.com/x-api-pricing/); [apiserpent](https://apiserpent.com/blog/best-x-twitter-api-providers-2026)

### Inferences
- For India, the reachable platforms are YouTube Shorts and Instagram Reels, plus Facebook Reels. Moj and Josh would need a manual "download and share" flow.
- X costs very little per post, but posts carrying a link cost 13 times more, so upload the video natively and leave links out.

### Gaps
- No search was done for Chingari, MX TakaTak (believed merged into Moj in 2022, from memory) or Josh developer programs.
- Snapchat Spotlight posting API (Snap's Public Profile or Creative Kit) was not researched.

## Unified posting APIs (shortcut)

### Takeaway
Several 2026 services post to YouTube, Instagram, TikTok and others through apps that have already passed review, so GCM Clipper could skip Meta App Review and the TikTok audit at first. The prices below come from vendor comparison pages and need confirming on each pricing page.

### Cited Findings
- **Zernio (formerly Late / getlate.dev):** rebranded in 2026 with usage pricing per connected account: first 2 accounts free, then $6 per account per month for accounts 3-10, $3 for 11-100 and $1 for 101 and up. — [Zernio blog](https://changelog.zernio.com/blog/unified-social-media-api); [Capterra](https://www.capterra.com/p/10036198/Late/)
- **Upload-Post:** claims unlimited posts from $24 a month, a free tier and 22 platforms. A competitor counts 11 platforms. These are vendor-written claims. — [Upload-Post comparison, Jul 2026](https://www.upload-post.com/best-social-media-apis); [Ayrshare vs Upload-Post](https://www.ayrshare.com/compare/upload-post-api-alternative/)
- **Ayrshare:** from $149 a month, priced per profile. It covers Instagram Business and Creator, TikTok, YouTube, X, Facebook and others. — [Ayrshare comparison](https://www.ayrshare.com/compare/upload-post-api-alternative/); [postproxy comparison](https://postproxy.dev/blog/best-social-media-scheduling-apis-compared/)
- **Using an already-audited app for TikTok:** vendors such as Blotato post through their own audited app. — [Blotato TikTok API](https://www.blotato.com/api/tiktok)
- **Postiz:** its docs show a self-hosted option, but self-hosting needs the developer's own app credentials, so the reviews still apply. — [Postiz TikTok provider docs](https://docs.postiz.com/self-host/providers/tiktok)

### Inferences
- Cheapest path with no review: do YouTube directly, since the private lock is gone and sensitive-scope verification takes 3-5 days and costs nothing. Use Zernio's free 2 accounts or Upload-Post's free tier for Instagram during beta. Apply for Meta review once a business is registered.
- Postiz is open source and free to self-host (AGPL, from memory). It saves building the scheduler UI but does not avoid platform reviews.

### Gaps
- Official pricing pages were not fetched, and whether the free tiers allow commercial use is unknown.
- Whether these services expose Instagram and YouTube analytics, and in how much detail, was not compared.

## Platform policy: automated posting, cross-posting, watermarks, game-audio copyright

### Takeaway
Instagram's April 2026 originality update pushes "unoriginal" reposts out of recommendations. Watermarks, small crops or speed changes do not count as original; "materially edited" content does. Clips should be the creator's own footage with real edits (captions, reframing, cuts), and should not carry other platforms' watermarks.

### Cited Findings
- **What counts as original:** Instagram treats "materially edited" content as original. Adding a watermark, changing speed or posting a screenshot with credit does not count. Reposted content from aggregators is left out of recommendations (Feed and Explore) but still reaches followers. — [TechCrunch, 30 Apr 2026](https://techcrunch.com/2026/04/30/instagram-restricts-reach-of-content-aggregators-in-new-crackdown/); [PetaPixel, 30 Apr 2026](https://petapixel.com/2026/04/30/new-instagram-policies-target-reposted-content/)
- **Scope and enforcement:** the policy grew from Reels-only to all content in April 2026. One outlet reports assessment on a rolling 30-day basis, and a threshold of 10 or more unoriginal posts in 30 days rests on unnamed insiders. — [PetaPixel](https://petapixel.com/2026/04/30/new-instagram-policies-target-reposted-content/); [WebProNews (weak source)](https://www.webpronews.com/instagrams-aggregator-purge-original-creators-gain-ground-as-repost-empires-crumble/)

### Inferences
- Posting the creator's own clip to YouTube, Instagram and X should not count as aggregation, because the creator owns the footage. Still, render a separate file per platform with no cross-platform watermark. Meta has long been reported to down-rank Reels carrying TikTok watermarks.

### Gaps
- No source was found on Content ID or Rights Manager matches for BGMI game audio or in-game music. This needs separate research, including Krafton's video content policy.
- YouTube's policy on automated or repetitious uploads (the "repetitious content" rule in the YouTube Partner Program) was not checked.
