# YouTube capabilities for a third-party gaming-creator app (as of November 2026)

Scope: what the YouTube Data API v3, Live Streaming API, Analytics/Reporting APIs and YouTube Studio let a third-party app (GCM Clipper) do, and which YouTube-native features overlap with planned features. Every claim carries the doc page it came from; "not found in docs" is stated where a doc was not located. Dates are the doc's own revision dates where given. Note: several developers.google.com fetches failed on the first try (network resets) and were retried; everything cited below was read from the page itself unless marked "secondary".

Quick verdict table (details and sources in the sections below):

| Planned GCM Clipper feature | API support | Notes |
|---|---|---|
| Upload Short, approve-then-post | Yes: `videos.insert` | Own daily bucket, default 100 uploads/day/project; upload privately then `videos.update` to public (50 units) |
| Scheduled publish | Yes: `status.publishAt` | Only on a private, never-published video; ISO 8601 datetime |
| Custom thumbnail on a Short | Yes since 3 Nov 2026: `thumbnails.set` | Only after `processingStatus == succeeded`; creator must be eligible (YPP per Studio rollout) |
| Upload captions | Yes: `captions.insert` (400 units) | Must include timing codes (`sync` deprecated) |
| Playlists / compilations | Yes: `playlists.insert`, `playlistItems.insert` (50 each) | |
| Made-for-kids / synthetic flags | Yes: `status.selfDeclaredMadeForKids`, `status.containsSyntheticMedia` | |
| Shorts "Related video" link | **No** | Studio only, needs advanced-feature access; use description + pinned comment (pinning also not in API) |
| Pinned comment | **Partial**: `commentThreads.insert` posts; **no pin** in API | Pin manually in Studio |
| End screens / cards / chapters | End screens & cards **no**; chapters **yes** via timestamps in description | |
| Community posts (create or read) | **No** | No resource in the Data API |
| Read live chat for "!clip" | Yes: `liveChatMessages.streamList` (push) or `.list` (poll, 5 units) | Works only while live |
| Bot reply in chat | Yes: `liveChatMessages.insert` (20 units) | |
| Chat replay of finished stream | **No official API** | `liveChatEnded` error after stream ends |
| Stream schedule / upcoming streams | Yes: `liveBroadcasts.list?mine=true&broadcastStatus=upcoming` (1 unit) | |
| Per-video analytics incl. Shorts | Yes: Analytics API (`video`, `creatorContentType`, `engagedViews`, `averageViewPercentage`, `subscribersGained`) | 48-72 h latency |
| Live concurrent viewers | Yes: Analytics `peakConcurrentViewers`/`averageConcurrentViewers`; Data API `liveStreamingDetails.concurrentViewers` while live | |
| Audience retention curve | Yes: Analytics audience retention report (`elapsedVideoTimeRatio`) | One video per query |

---

## Key question 1: Can the API set the Shorts "Related video" link? What are the alternatives?

### Takeaway
No. The related-video link is a YouTube Studio feature with no corresponding field in the `videos` resource; the only API-side alternatives are a URL in the description (not clickable in the Shorts player) and a top-level comment via `commentThreads.insert`, which the API cannot pin. End screens and cards also have no API.

### Cited Findings
- Studio's "Add a related video to your YouTube Shorts" page describes the feature only as Studio steps: Content > click the Short > "Select a Related Video from your channel" > SAVE. It says the feature "allows you to showcase your Videos, Shorts, and Live in the Shorts player", that "Adding a related video is only available with advanced feature access", and the target "has to be public or unlisted and must follow our Community Guidelines." — [YouTube Help: Add a related video to your YouTube Shorts](https://support.google.com/youtube/answer/14075157)
- The `videos` resource reference lists no related-video, end-screen or card property; the only linking-adjacent fields are `snippet.liveBroadcastContent`, `liveStreamingDetails.*`, and chapters, which are created "by including formatted timestamps" in `snippet.description`. — [YouTube Data API: Videos resource](https://developers.google.com/youtube/v3/docs/videos)
- Secondary confirmation from a competitor's help page: Opus Clip tells users YouTube "does not yet allow this to be done through their public API", so the related link must be added manually in Studio. — [Opus Clip help: Link Shorts to original video](https://help.opus.pro/docs/article/link-shorts-to-original-video) (secondary; vendor)
- Vevo's support note: URLs in Shorts descriptions and comments are not clickable. — [Vevo support: YouTube Shorts](https://support.vevo.com/hc/en-us/articles/53791074157083-YouTube-Shorts) (secondary)
- `commentThreads.insert` "Creates a new top-level comment", costs 50 units, requires the `youtube.force-ssl` scope, requires `snippet.channelId`, `snippet.videoId` and `snippet.topLevelComment.snippet.textOriginal`, and "lists no pinning or moderation parameters." — [YouTube Data API: commentThreads.insert](https://developers.google.com/youtube/v3/docs/commentThreads/insert)
- No official page for a pin-comment API was found; community threads (Pipedream, Stack Overflow) only reference `comments.insert` and `commentThreads.insert`. — [Pipedream community thread](https://pipedream.com/community/t/how-to-specify-video-type-in-youtube-video-upload-api-to-avoid-automatic-conversion-to-shorts/8897?page=2) (secondary)
- No official endpoint for end screens or cards exists; community posts from 2015 and 2023 say there is "no way to manage Cards in the API", and an "Unofficial YouTube Studio API" project exists precisely to fill the end-screen gap using Studio session cookies. — [Stack Overflow 2015 (mirror)](https://kiwix.lema.org/stackoverflow.com_en_all_2023-11/questions/29819716/youtube-cards-api); [Stack Overflow 2023 (mirror)](https://kiwix.lema.org/stackoverflow.com_en_all_2023-11/questions/75170801/add-cards-to-video-with-youtube-api); [adasq/youtube-studio (GitHub)](https://www.Github.com/adasq/youtube-studio) (all secondary)
- YouTube's own Developer Policies forbid working around that: API clients must "not access or use the YouTube API Services in a manner that is deceptive" (ToS §5) and must not circumvent quota/use restrictions (§15). — [YouTube API Services Terms of Service](https://developers.google.com/youtube/terms/api-services-terms-of-service)

### Inferences
- GCM Clipper should post the Short via API, then show the creator a one-tap "open in Studio to add the related video" deep link (Studio URL for the video) plus pre-filled copy; the app cannot complete this step itself.
- Using the unofficial Studio API (cookie/session scraping) would violate the API ToS and risk the channel; do not build on it.
- A top-level comment with the stream link can be posted by the app, but the creator must pin it manually.

### Gaps
- No official YouTube statement was found on whether the related-video link will ever be exposed via API; the Data API revision history through 3 Nov 2026 contains no such entry.
- Whether the Nov 2026 Shorts player shows the related link for streams scheduled in the future (teaser Short -> upcoming stream) is not stated on the help page; it only says Videos, Shorts and Live.

---

## Key question 2: videos.insert, quota, publishAt, thumbnails for Shorts, captions, playlists, made-for-kids and synthetic-content fields

### Takeaway
Uploads now live in their own quota bucket (default 100 `videos.insert` calls per project per day, 1 unit each), scheduling works only on a private, never-published video via `status.publishAt`, Shorts custom thumbnails became settable through `thumbnails.set` on 3 Nov 2026, captions cost 400 units and must carry timings, and both `selfDeclaredMadeForKids` and `containsSyntheticMedia` are settable on insert/update.

### Cited Findings
**Quota and buckets**
- "June 1, 2026 (quota): The API moves to granular quota buckets. videos.insert and search.list each get their own bucket, and all other methods stay in the existing bucket." "June 3, 2026: The new videos.batchGetStats method ... Each call costs 1 unit in its own granular quota bucket, with a default of 10,000 units per day." "December 4, 2025: The documented quota cost of a video upload drops from about 1,600 units to about 100 units." — [Data API revision history](https://developers.google.com/youtube/v3/revision_history)
- Quota page: projects get "10,000 units per day for all endpoints other than search.list and videos.insert"; "search.list and videos.insert each have their own bucket, with a default limit of 100 calls per day"; quotas reset at midnight Pacific Time. Costs: videos.insert 1 (in the 100/day bucket); videos.update 50; videos.list 1; thumbnails.set 50; captions.insert 400; commentThreads.insert 50; comments.insert 50; comments.setModerationStatus 50; playlists.insert 50; playlistItems.insert 50; liveBroadcasts.list 1; liveChatMessages.list 5; liveChatMessages.insert 20; search.list 1 (in the 100/day bucket); channels.list 1. — [Quota calculator](https://developers.google.com/youtube/v3/determine_quota_cost)
- videos.insert page: "Quota impact: 100 calls per day", scopes any of `youtube.upload`, `youtube`, `youtubepartner`, `youtube.force-ssl`; max file size 256 GB; `notifySubscribers` defaults to true; error `uploadLimitExceeded` (400) means the user "has exceeded the number of videos they may upload" (no number given). — [videos.insert](https://developers.google.com/youtube/v3/docs/videos/insert)
- Audit page: default allocation is "100 search.list calls, 100 videos.insert calls" plus the unit limit for other endpoints; more quota requires "an audit to show that your project is in compliance" via the "YouTube API Services - Audit and Quota Extension Form"; a periodic audit form exists; appeals form exists for failed audits. — [Quota and compliance audits](https://developers.google.com/youtube/v3/guides/quota_and_compliance_audits)

**Privacy default and unverified projects**
- "November 2, 2026: Videos uploaded through videos.insert from unverified projects are no longer forced to private. This reverses the July 28, 2020 policy. If no privacy status is given, the default is public, though creator settings can make some uploads private." — [Data API revision history](https://developers.google.com/youtube/v3/revision_history); videos.insert page now says "Videos uploaded from unverified API projects are not restricted to private viewing mode." — [videos.insert](https://developers.google.com/youtube/v3/docs/videos/insert)

**Scheduling**
- `status.publishAt`: "The date and time when the video is scheduled to publish." "This property can only be set if the video's privacy status is `private` and the video has never been published." If the time is in the past "the video will be published right away." — [Videos resource](https://developers.google.com/youtube/v3/docs/videos)
- Settable on insert: `status.publishAt`, `status.selfDeclaredMadeForKids`, `status.containsSyntheticMedia`, plus `snippet.title/description/tags/categoryId/defaultLanguage`, `localizations`, `recordingDetails.recordingDate`. — [videos.insert](https://developers.google.com/youtube/v3/docs/videos/insert)

**Thumbnails (incl. Shorts)**
- "November 3, 2026: The thumbnails.set method can now upload custom thumbnails for YouTube Shorts after processing finishes. The thumbnails resource adds a `shortsAspectRatio` property." "September 14, 2026: The maximum file size for thumbnails.set ... rises from 2MB to 50MB." — [Data API revision history](https://developers.google.com/youtube/v3/revision_history)
- thumbnails.set: "approximately 50 units"; scopes `youtubepartner`, `youtube.upload`, `youtube`, `youtube.force-ssl`; max 50 MB; `image/jpeg`, `image/png`; for Shorts call it "only after the video has finished processing" (`processingDetails.processingStatus == succeeded`), otherwise "the custom thumbnail might not be applied to the Short"; errors include 403 "doesn't have permissions to upload and set custom video thumbnails" and 429 `uploadRateLimitExceeded` "The channel has uploaded too many thumbnails recently." — [thumbnails.set](https://developers.google.com/youtube/v3/docs/thumbnails/set)
- Studio side: "YouTube Partner Program creators can start uploading custom thumbnails for Shorts", "We'll expand this to more creators over time", desktop offers "three suggested thumbnail frames"; post dated July 24, 2026. — [YouTube Blog: Making thumbnails easier on YouTube](https://blog.youtube/news-and-events/youtube-studio-custom-thumbnail-updates/)

**Captions**
- captions.insert: "quota cost of 400 units"; scopes `youtube.force-ssl` or `youtubepartner`; max 100 MB; required `snippet.videoId`, `snippet.language`, `snippet.name`; `snippet.isDraft` optional; `sync` parameter "has been deprecated". — [captions.insert](https://developers.google.com/youtube/v3/docs/captions/insert)
- "March 13, 2024: The sync parameter for captions.insert and captions.update is deprecated, effective April 12, 2024. Caption uploads must now include timing information or they fail." "March 12, 2024: The maximum length of snippet.name for caption tracks is 150 characters." — [Data API revision history](https://developers.google.com/youtube/v3/revision_history)

**Made for kids / synthetic content**
- `status.selfDeclaredMadeForKids`: "allows the channel owner to designate the video as being child-directed"; "only returned if the channel owner authorized the API request." `status.madeForKids` "indicates whether the video is designated as child-directed" and "might be determined based on the value of the selfDeclaredMadeForKids property." — [Videos resource](https://developers.google.com/youtube/v3/docs/videos)
- "October 15, 2026: videos.list now clarifies that status.selfDeclaredMadeForKids and status.madeForKids change only when included in the request." "October 30, 2024: The videos resource adds status.containsSyntheticMedia to flag realistic altered or synthetic content. It can be set through videos.insert or videos.update." — [Data API revision history](https://developers.google.com/youtube/v3/revision_history)
- `status.containsSyntheticMedia` "allows the channel owner to disclose that a video contains realistic" altered or synthetic content, e.g. videos that "Alter footage of a real event or place." — [Videos resource](https://developers.google.com/youtube/v3/docs/videos)
- Other 2026 Data API changes relevant to the app: July 7, 2026 `brandPartner` part on videos; Aug 27, 2026 public view counting aligned across long-form, Live and Shorts (view counted when playback begins; "Monetization stays tied to engaged metrics"); Sept 11, 2026 higher-res thumbnail keys `fhd`, `qhd`, `uhd`; Sept 30, 2026 `snippet.imageUrl` on comments. — [Data API revision history](https://developers.google.com/youtube/v3/revision_history)

**What makes an upload a Short**
- Studio help: creators can "create Shorts up to three minutes long." — [YouTube Help: Create Shorts](https://support.google.com/youtube/answer/10343433)
- A/B-testing help page: uploads "up to three minutes long that are square or taller are classified as Shorts." — [YouTube Help: A/B test titles & thumbnails](https://support.google.com/youtube/answer/16391400)
- No `isShort` flag exists in the `videos` resource. — [Videos resource](https://developers.google.com/youtube/v3/docs/videos)

### Inferences
- Approve-then-post flow that fits the rules: `videos.insert` with `privacyStatus=private` and optional `publishAt`, then (if the creator approves later) `videos.update` to `public`. Cost per clip: 1 upload-bucket call + 50 (update) + 50 (thumbnail) + 400 if captions are uploaded as a track rather than burned in. With burned-in captions and no caption track, ~100 units per clip, so the 10,000-unit bucket allows ~100 clips/day across all users of the project, and the 100-upload bucket is the harder cap across all connected creators until a quota extension/audit is passed.
- Because `publishAt` requires a never-published private video, "reschedule" must be done by updating `publishAt` on the still-private video, not by re-privatising a published one.
- `containsSyntheticMedia` should stay `false` for ordinary clips (captions, crops, colour, overlays are explicitly "minor edits"; see Q6), but the app should expose the toggle for AI voice-overs or AI-generated scenes.

### Gaps
- The per-channel upload limit behind `uploadLimitExceeded` is not published anywhere in the docs.
- The `shortsAspectRatio` property's allowed values were not visible on the thumbnails.set page at fetch time (only the revision-history entry mentions it).
- Whether thumbnails.set for Shorts needs the channel to be in YPP (as the Studio rollout does) is not stated on the API page; the 403 permission error is the only hint.

---

## Key question 3: Live chat ("!clip" markers), bot replies, chat replay, and the creator's stream schedule

### Takeaway
Reading live chat in real time is officially supported (streamList push, or list polling at 5 units with a server-supplied `pollingIntervalMillis`), bot replies cost 20 units, upcoming streams are a 1-unit `liveBroadcasts.list` call, but there is no official way to read the chat replay of a finished stream: both chat methods fail with `liveChatEnded` once the broadcast is over.

### Cited Findings
- `liveChatMessages.list`: "quota cost of 5 units"; `liveChatId` comes from the broadcast's `snippet.liveChatId`; `maxResults` 200-2000 (default 500); response has `pollingIntervalMillis` = "The amount of time, in milliseconds, that the client should wait before polling again" and `offlineAt` "only present if the stream is already offline"; error `liveChatEnded` (403) "The specified live chat is no longer live." The page itself says to poll for messages you should use `liveChatMessages.streamList`, "which pushes new messages to the client as they become available." — [liveChatMessages.list](https://developers.google.com/youtube/v3/live/docs/liveChatMessages/list)
- `liveChatMessages.streamList` "establishes a server-streaming connection" and "pushes new messages to your client as soon as they are available"; "quota cost of 5 units"; on connect it sends recent history; `pageToken` can resume a dropped stream; too-frequent reconnects return RESOURCE_EXHAUSTED / `rateLimitExceeded`; after the stream ends: "You can't retrieve messages for the ended live chat" (LIVE_CHAT_ENDED). — [liveChatMessages.streamList](https://developers.google.com/youtube/v3/live/docs/liveChatMessages/streamList)
- `liveChatMessages.insert`: "quota cost of 20 units"; scopes `youtube` or `youtube.force-ssl`; requires `snippet.liveChatId`, `snippet.type` (`textMessageEvent` or `pollEvent`) and `snippet.textMessageDetails.messageText`; errors `rateLimitExceeded` "The user has posted too many chat messages in a given timeframe", `liveChatDisabled`, `liveChatEnded`. — [liveChatMessages.insert](https://developers.google.com/youtube/v3/live/docs/liveChatMessages/insert)
- June 23, 2026 revision: references to `messageDeletedEvent` and `messageRetractedEvent` removed from liveChatMessages "since the API no longer returns them." — [Data API revision history](https://developers.google.com/youtube/v3/revision_history)
- `liveBroadcasts.list`: filters `broadcastStatus` (`active`, `all`, `completed`, `upcoming`), `id`, or `mine=true`; `broadcastType` `all`/`event`(default)/`persistent`; `maxResults` 0-50; scopes `youtube.readonly`, `youtube`, `youtube.force-ssl`; 1 unit per the quota page. — [liveBroadcasts.list](https://developers.google.com/youtube/v3/live/docs/liveBroadcasts/list); [Quota calculator](https://developers.google.com/youtube/v3/determine_quota_cost)
- `liveBroadcast` resource: `snippet.scheduledStartTime` ("Unix epoch time zero" if unset), `snippet.actualStartTime` (only once `live`), `snippet.liveChatId`, `status.lifeCycleStatus` values `complete`, `created`, `live`, `liveStarting`, `ready`, `revoked`, `testStarting`, `testing`; `contentDetails.enableDvr` default true; `contentDetails.recordFromStart` default true; no vertical/dual-format or Shorts field (`projection` is only `360`/`rectangular`). — [liveBroadcasts resource](https://developers.google.com/youtube/v3/live/docs/liveBroadcasts)
- Videos resource, for stream-to-VOD mapping: `liveStreamingDetails.activeLiveChatId` "filled only if the video is a currently live broadcast that has live chat ... Once the broadcast transitions to complete this field will be removed and the live chat closed down"; `liveStreamingDetails.concurrentViewers` "YouTube stops tracking the number of concurrent viewers for a broadcast when the broadcast ends"; `liveStreamingDetails` "will only be present ... if the video is an upcoming, live, or completed live broadcast." — [Videos resource](https://developers.google.com/youtube/v3/docs/videos)

### Inferences
- "!clip" markers must be captured while the stream is live (streamList connection or 5-unit polls at the server's interval); the app should store the marker timestamps itself, keyed to `actualStartTime`, because there is no post-stream chat API. A full day of polling at e.g. 5 s intervals would cost ~86,000 units, far over the 10,000 default, so streamList (one 5-unit call per connection) is the only viable approach without a quota extension.
- A bot reply ("Clip saved!") costs 20 units each; cap replies per stream to avoid both quota burn and the `rateLimitExceeded` error.
- Upcoming streams for the schedule screen: `liveBroadcasts.list?mine=true&broadcastStatus=upcoming&broadcastType=all` (1 unit). The VOD of a finished stream is the same video id as the broadcast id.
- `recordFromStart`/`enableDvr` being true by default means most creators' archives will exist and be clippable after the stream; the app should warn if a creator disabled archiving.

### Gaps
- Numeric rate limit for `liveChatMessages.insert` and for streamList reconnects is not published.
- No official doc describes any chat-replay endpoint; the "live chat replay" seen on YouTube watch pages is an internal (InnerTube) feature only. Scraping it would fall under ToS §5/§15 concerns.
- The liveBroadcasts.list page does not restate its quota cost; the 1-unit figure comes from the quota calculator page.

---

## Key question 4: Analytics API and Reporting API: per-video metrics for Shorts vs long, live metrics, retention, dimensions, data delay

### Takeaway
The Analytics API gives per-video views, `engagedViews`, `averageViewDuration`, `averageViewPercentage`, `subscribersGained`, split by `creatorContentType` (SHORTS / LIVE_STREAM / VIDEO_ON_DEMAND), plus `peakConcurrentViewers`/`averageConcurrentViewers` for live and a 100-point audience-retention curve per video; data lags 48-72 hours, and the Reporting API gives bulk daily CSVs available within 48 hours of job creation and retained 60 days.

### Cited Findings
**Metrics**
- `engagedViews`: "The number of times the channel's videos have been viewed past the first frame, or the user clicks/taps to play." `averageViewDuration`: average length in seconds of playbacks (since Dec 13, 2021 excludes looping-clip traffic). `averageViewPercentage`: average percentage of a video watched. `subscribersGained`: reports filtered to a single video "count only subscriptions from that video's watch page." `estimatedMinutesWatched`, `audienceWatchRatio` (can exceed 1 on rewatch), `relativeRetentionPerformance` (0-1, 0.5 = median vs similar-length videos), `averageConcurrentViewers`, `peakConcurrentViewers` ("The peak number of concurrent viewers for a particular video", with `livestreamPosition` dimension for segments). "Shorts-specific metrics: None are defined." — [Analytics API metrics](https://developers.google.com/youtube/analytics/metrics)
- Video report basic metrics list includes engagedViews, views, comments, likes, dislikes, shares, estimatedMinutesWatched, averageViewDuration, averageViewPercentage, subscribersGained, subscribersLost, card metrics; monetary metrics require `yt-analytics-monetary.readonly` and YPP membership. — [Channel reports](https://developers.google.com/youtube/analytics/channel_reports)

**Dimensions**
- `creatorContentType` "identifies the type of content associated with the user activity metrics in the data row"; values `LIVE_STREAM`, `SHORTS`, `STORY`, `VIDEO_ON_DEMAND`, `UNSPECIFIED`; data from Jan 1, 2019. `liveOrOnDemand` values `LIVE`, `ON_DEMAND`. `elapsedVideoTimeRatio` returns "100 data points per video, with values from 0.01 to 1.0". `audienceType` (filter only) `ORGANIC`, `AD_INSTREAM`, `AD_INDISPLAY`. `insightTrafficSourceType` e.g. `YT_SEARCH`, `EXT_URL`, `SUBSCRIBER`. `subscribedStatus`, `youtubeProduct`, `day`. Reports return data "up until the last day for which all metrics specified in the request are available." — [Analytics API dimensions](https://developers.google.com/youtube/analytics/dimensions)

**Audience retention**
- Required dimension `elapsedVideoTimeRatio`; metrics `audienceWatchRatio`, `relativeRetentionPerformance`, `startedWatching`, `stoppedWatching`, `totalSegmentImpressions`; required filter `video`; optional `audienceType`, `subscribedStatus`, `youtubeProduct`; the report "does not support the ability to specify a comma-separated list of values for the video filter." — [Channel reports](https://developers.google.com/youtube/analytics/channel_reports)
- Analytics revision history: "May 6, 2024: Adds three channel reports, including Concurrent viewers for live-streamed videos, and three Audience Retention metrics." — [Analytics API revision history](https://developers.google.com/youtube/analytics/revision_history)

**Data latency**
- "Data processing typically introduces a latency of 48 to 72 hours." "API responses do not contain data for the most recent days." "the underlying analytics data is not real-time." Discrepancies vs Studio's real-time metrics are expected. — [Analytics API data model](https://developers.google.com/youtube/analytics/data_model)

**2025-2026 Analytics changes**
- "March 26, 2025: Announces the Shorts view-counting change and the new engagedViews metric." "April 24, 2025: Targeted Queries gain the Shorts view change and engagedViews, effective April 30, 2025." "June 24, 2025: Bulk Reports get new versions for view-based reports, an engaged_views column." "August 27, 2026: Aligns public view counting across long-form, Live, and Shorts. Views count from the first frame, and the engagedViews metric definition is updated." "June 25, 2026: Removes the User activity by city report for content owners." "September 13, 2026: Adds Version 1.1 of the weekly references report." — [Analytics API revision history](https://developers.google.com/youtube/analytics/revision_history)
- "November 15, 2024: Traffic Source queries fail when videos multiplied by days exceed 50,000." — [Analytics API revision history](https://developers.google.com/youtube/analytics/revision_history)

**Reporting API (bulk)**
- "You can start retrieving the report within 48 hours of the time that the job is created." "Reports are updated daily." "API reports are available for 60 days from the time that they are generated." "Reports containing historical data are available for 30 days from the time that they are generated." Example report `channel_basic_a3`. No quota/pricing stated. — [Reporting API: reports](https://developers.google.com/youtube/reporting/v1/reports)

### Inferences
- A "Shorts vs long-form" dashboard is one query: dimensions `video`, filter `creatorContentType==SHORTS`, metrics `views,engagedViews,averageViewDuration,averageViewPercentage,subscribersGained,likes,shares`. Live streams come from `creatorContentType==LIVE_STREAM` with `peakConcurrentViewers`.
- Retention curves for "best moment" detection need one request per video (100 points each) and are only available 2-3 days after the stream; this is useful for ranking old VODs, not for same-day clipping.
- The app should always query with `endDate` at least 3 days back and show "data through <date>" to avoid confusing creators comparing with Studio.

### Gaps
- Whether `peakConcurrentViewers` is available with the `video` dimension for a single stream (vs only the channel-level concurrent-viewers report) was not verified on the channel_reports page (page truncated).
- Reporting API quota limits were not found in the docs read.

---

## Key question 5: Community posts (create / read / polls) via API

### Takeaway
There is no Data API resource for posts or polls; the `activities` resource stopped carrying channel discussions in 2024, and Google's own tracker shows the request as unresolved. Posts and polls must be made in YouTube's app or Studio.

### Cited Findings
- Data API revision history: "April 30, 2024 (deprecation): The API no longer supports inserting or retrieving channel discussions." — [Data API revision history](https://developers.google.com/youtube/v3/revision_history)
- Google Issue Tracker thread asks for community-post API access and notes there "is no access to community posts through any of the API." — [issuetracker.google.com/issues/405004980](https://issuetracker.google.com/issues/405004980) (user-filed; secondary)
- Zapier and Make community threads conclude YouTube hasn't opened its API for community posts. — [Zapier community](https://community.zapier.com/how-do-i-3/zapping-posts-to-youtube-community-section-workaround-20931); [Make community](https://community.make.com/t/youtube-community-posts/83412) (secondary)
- Studio-side facts: posts support "polls, quizzes, GIFs, text, music, images, and video"; scheduled posts appear in YouTube Studio; not available if channel is "Made for Kids" or supervised; "posts aren't currently available in Germany." — [YouTube Help: Learn about posts](https://support.google.com/youtube/answer/9409631)
- "We limit how many posts a channel can create in a 24-hour period." — [YouTube Help: Create a post](https://support.google.com/youtube/answer/7124474)
- Feature access (posts, custom thumbnails, etc.) is listed under Studio > Settings > Channel > Feature eligibility. — [YouTube Help: Feature access](https://support.google.com/youtube/answer/9890437)

### Inferences
- GCM Clipper can only draft post text/poll options and hand them to the creator with a "copy and post" step; scheduling must use Studio's own scheduler.

### Gaps
- The current subscriber threshold for Posts eligibility was not stated on the official pages read (the 2021 "500 subscribers" rule may be outdated).

---

## Key question 6: YouTube Studio native features and their 2026 status (overlap with GCM Clipper)

### Takeaway
YouTube now auto-generates highlight Shorts only for vertical mobile-app streams (10 min-12 h, chat on), lets owners clip their own archived streams/videos into 5-60 s Clips and convert them to Shorts, offers Test & Compare (3 titles/thumbnails, watch-time winner, desktop, long-form only, not Shorts), Ask Studio (web only, most creators globally), auto-dubbing from Hindi to English and Bengali, Hype (YPP, 500-500k subs, India included, Shorts excluded), Communities (mobile, needs Posts access), Shorts up to 3 min with YPP-only custom thumbnails, and dual-format live with a vertical copy surfacing in the Shorts feed. None of these covers automatic 9:16 clipping of a desktop/encoder gaming stream, which remains the app's gap to fill.

### Cited Findings
**Auto highlight Shorts from live streams**
- "The live stream must be between 10 minutes and 12 hours." "The stream must be in a vertical format and streamed using the YouTube mobile app." "The stream cannot be a screencast." "The stream has chat enabled." "The stream must not be set as 'Made for Kids.'" After a mobile stream you can "save a Short highlight video, which is automatically pulled from your live stream"; it is saved as a private video you can make public. — [YouTube Help: Promote your live stream](https://support.google.com/youtube/answer/2524542)
- Secondary: at Made on YouTube (Sept 16, 2025) YouTube announced AI-generated highlight Shorts from live streams and dual-format streaming. — [Social Media Today](https://www.socialmediatoday.com/news/youtube-adds-reply-filters-live-stream-highlights-shorts/760959/); [Dexerto](https://jamtest.dexerto.com/youtube/youtube-launches-ai-powered-highlight-tool-to-automatically-create-stream-clips-3252018) (secondary)
- Stream markers: during a live broadcast you can add a stream marker; markers appear on the timeline when making a highlight in YouTube Editor. — [YouTube Help: Create a highlight](https://support.google.com/youtube/answer/4522163)

**Clips (archived streams and videos)**
- Clips are 5-60 seconds, public, created in the YouTube app (viewers) or YouTube Studio / Studio app (creators on their own videos or streams); "You can't create Clips from live streams without DVR or live streams longer than the DVR timeframe"; clips from live streams appear only after the stream ends; source-video owners "can convert the entire clip into a Short"; "Clipping videos is turned on by default." — [YouTube Help: Create & manage Clips](https://support.google.com/youtube/answer/10332730)

**Test & Compare / A/B testing**
- "Creators can test and compare up to 3 different titles and thumbnails"; the winner is "the title or combination of title and thumbnail with the highest watch time"; "Your test should be completed within two weeks"; "Desktop only"; requires advanced features; "You are not able to A/B test Shorts, Scheduled Lives, and Premiere videos at this time"; "A/B testing is not available for Shorts"; live archives can be tested; not for made-for-kids, mature or private videos. — [YouTube Help: A/B test titles & thumbnails](https://support.google.com/youtube/answer/16391400); thumbnail-only page: [Test & compare thumbnails](https://support.google.com/youtube/answer/13861714)

**Ask Studio**
- Helps "brainstorm video ideas, get channel insights, and analyze your performance"; usable on the Analytics page; prompt "Summarize comments"; up to 10 images can be uploaded to "generate reference thumbnails"; "available only on web browsers on your computer"; "available to most YouTube creators globally" except Official Artist Channels, Made for Kids channels and under-18s; conversations kept "for 30 days." — [YouTube Help: Learn about Ask Studio](https://support.google.com/youtube/answer/16291691)
- Ask Studio can generate thumbnails for long-form videos ("Simply ask for a thumbnail for your latest video"), July 24, 2026. — [YouTube Blog](https://blog.youtube/news-and-events/youtube-studio-custom-thumbnail-updates/)
- Secondary: Ask Studio expanding to the Studio mobile app in fall 2026 (Made on YouTube 2026 coverage). — [uppbeat.io summary](https://uppbeat.io/blog/creator-news/made-on-youtube-2026-brings-new-youtube-tools-for-editing-earning-and-more) (secondary)

**Auto-dubbing (Hindi)**
- Hindi source videos get dubs in "Bengali, English*" (asterisk = expressive speech); Hindi is also a target for English-source videos; "This feature is enabled by default for eligible creators"; ineligible if longer than 120 minutes, little speech, undetectable language, speech too fast, or copyright claim; "Publish manually" option to review dubs; per-dub management only on desktop Studio; no mention of Shorts or live. — [YouTube Help: Use automatic dubbing](https://support.google.com/youtube/answer/15569972)
- Live auto-dubbing: a pilot "starting in early 2027." — [YouTube Blog: Live tools (Sept 23, 2026)](https://blog.youtube/news-and-events/made-on-youtube-live-tools-fan-funding-dubbing/)
- Secondary: Feb 2026 coverage says auto-dubbing expanded to all users with 27 languages. — [India TV News](https://www.indiatvnews.com/technology/news/youtube-auto-dubbing-feature-expands-to-all-users-now-supports-27-languages-2026-02-05-1029070) (secondary)

**Hype**
- "Channels in the YouTube Partner Program with 500 to 500,000 subscribers are eligible"; India is in the availability list; cannot hype age-restricted, unlisted/private, made-for-kids, copyright-claimed videos or YouTube Shorts; live streams/Premieres excluded while live but the archive becomes eligible; Hype window is the first 7 days after publish; opt-out in Studio desktop or mobile. — [YouTube Help: Hyping videos eligibility](https://support.google.com/youtube/answer/15509925)

**Communities and Posts**
- "You can start your own Community if: You have existing access to posts; You're over 16 and your channel is not set up as a supervised experience; Your audience is not set as made for kids; Your channel is not a VEVO channel"; steps are in the YouTube mobile app; subscribers must be subscribed for a minimum period before posting. — [YouTube Help: Start your Community](https://support.google.com/youtube/answer/15739414); viewer side: [Participate in Communities](https://support.google.com/youtube/answer/15739409)
- Secondary: Communities expanded to all creators with Posts access, mobile-only. — [ppc.land](https://ppc.land/youtube-expands-communities-feature-to-all-eligible-creators/) (secondary)

**Shorts length, thumbnails, series**
- Shorts "up to three minutes long." — [YouTube Help: Create Shorts](https://support.google.com/youtube/answer/10343433)
- Custom Shorts thumbnails: YPP creators first, desktop picks from three suggested frames, mobile any frame; July 24, 2026. — [YouTube Blog](https://blog.youtube/news-and-events/youtube-studio-custom-thumbnail-updates/)
- Made on YouTube 2026 (Sept 23, 2026): "conversational AI editing partner in Shorts", "better feedback in YouTube Studio", likeness detection expansion, custom mood feeds, "structured Shorts series on TV". — [Google Blog: Made on YouTube 2026](https://blog.google/products-and-platforms/products/youtube/made-on-youtube-updates-2026/)

**Vertical live, dual-format, "Watch Live" in the Shorts feed**
- Dual stream: "The vertical stream is a center crop of the horizontal stream, with other vertical layout options available below"; a second stream key is used for the vertical stream; "The same live chat is shown to viewers of both your horizontal and vertical streams"; "You can't add the vertical format once the stream has started"; Dual stream can be turned off in Stream settings; "Viewers (not limited to existing channel subscribers) can also find these live streams when browsing YouTube Shorts"; live streaming requires no restrictions in the past 90 days and a verified channel. — [YouTube Help: Get started with live streaming](https://support.google.com/youtube/answer/2474026)
- Viewer side: "you may find live streams in a vertical format" while browsing Shorts; "You can also enter the vertical live feed by tapping Pause on a Short, and tapping the Live button"; "Scheduled live streams and Premieres won't show up in the vertical live feed"; not on tablets. — [YouTube Help: Watch & interact with vertical live streams](https://support.google.com/youtube/answer/13822251)
- Secondary: dual-format streaming reached third-party encoders on Aug 20, 2026; the vertical feed lacks clickable links and live ads. — [ppc.land](https://ppc.land/encoders-gain-youtube-dual-streaming-as-vertical-feed-lacks-5-of-9-features/) (secondary)
- 2026-2027 Live roadmap: "React live" on eligible long-form videos/livestreams rolling out "later this year"; "Go Live Together" co-host matchmaking "In early 2027"; "Live showdown" "coming in 2027"; live auto dubbing pilot "early 2027". — [YouTube Blog: Live tools (Sept 23, 2026)](https://blog.youtube/news-and-events/made-on-youtube-live-tools-fan-funding-dubbing/)

**YouTube Create app (India)**
- Official availability page lists India among Android countries (phones with at least 4 GB RAM); iPhone availability narrower. — [YouTube Help: YouTube Create available locations](https://support.google.com/youtube/answer/13952912)
- Secondary: launched in India in beta March 2024; "Edit with AI" extended to all YouTube Create users in India. — [Business Today 2024](https://www.businesstoday.in/technology/story/youtube-create-app-now-available-in-india-lets-you-edit-videos-on-mobile-420228-2024-03-05); [BuzzInContent](https://www.buzzincontent.com/news/youtube-expands-ai-led-creation-discovery-and-safety-tools-for-india-creators-10785200) (secondary)

### Inferences
- YouTube's own highlight Shorts need a vertical, mobile-app stream with chat; a BGMI creator streaming 16:9 from a PC/emulator through OBS gets no auto highlights from YouTube, which is exactly the GCM Clipper case. Even with dual-format on, the highlight criteria page still says "streamed using the YouTube mobile app."
- Native Clips are 60 s max, 1:1 trim of the original frame (no 9:16 reframing, captions or ranking), and must be made by hand in Studio; they overlap only with a "manual clip" fallback.
- Test & Compare does not apply to Shorts, so an in-app "which caption/hook performed better" comparison for Shorts has no native equivalent; but for long VODs the app should not rebuild thumbnail testing.
- Hype excludes Shorts; auto-dubbing has no Shorts mention; so the app's Hindi/English caption work is not duplicated by YouTube for Shorts.
- Since Studio now has custom Shorts thumbnails (YPP) and the API supports them since 3 Nov 2026, the app can set a thumbnail from the clip's best frame; non-YPP creators will likely get a 403 and should fall back to YouTube's auto frame.

### Gaps
- No official help page was found for the AI-generated (vs rule-based) live highlights announced Sept 2025; the help page only lists the criteria above and does not say whether desktop/encoder streams will ever be eligible.
- "Shorts remix of live streams" has no dedicated official page found; the Clips page only says clips can be remixed into Shorts if the source is remix-eligible.
- Whether the "Watch Live" label still exists in Nov 2026 is unconfirmed; the current help page calls it the "Live button."
- YouTube Create's 2026 India-specific feature list could not be confirmed from an official page.

---

## Key question 7: Policies that constrain an auto-posting app

### Takeaway
The Developer Policies allow uploads and comments on a user's behalf only with the user's "prior specific and express consent" and "final control" over what is published, cap stored Authorized Data at 30 days unless refreshed, forbid selling API data or access, and any quota beyond the default triggers a compliance audit; YouTube's monetisation policy renamed "repetitious content" to "inauthentic content" (July 15, 2025) and treats compilations with no commentary as reused content, while the synthetic-content label is required only for realistic alterations and not for captions, colour or filters.

### Cited Findings
**Developer Policies (sections quoted)**
- III.E.4.c: "After 30 calendar days, the API Client must either delete or refresh the stored data." III.E.4.b: an API client "must still ensure every 30 days that it is still authorized by the user to access that data" (Analytics/Reporting/statistics stored longer) and "must not store statistics retrieved as Non-Authorized Data for more than 30 days." III.E.4.e: "must use reasonable efforts to ensure that their stored API Data is consistent with the current data." — [YouTube API Services Developer Policies](https://developers.google.com/youtube/terms/developer-policies)
- III.G.1.a: may not "sell, purchase, lease, lend, convey, redistribute, or sublicense all or any portion of" YouTube API Services; III.G.1.b: selling access requires YouTube's prior written approval. — same page
- III.C.3: "users must have final control over the data that will be published to YouTube Applications." III.E.3.d: for actions that insert, share, update or delete content, "the user must expressly consent to those actions prior to their actual execution." III.I.2: clients "must not automate or trigger views, uploads, comments, likes, dislikes, or other actions" without "the user's prior specific and express consent." III.I.11: must not "spam ... or harass anyone." — same page
- III.D.3: "YouTube may use quotas and place use restrictions"; to get more quota you "can apply for a quota extension by completing an API Compliance Audit"; III.H: YouTube "reserves the right to survey, monitor, and/or audit"; III.H.3: on request you must "provide YouTube with account(s) necessary to access all features or functions" of production clients. III.F.2.a: displayed content must "make clear to the viewer that YouTube is the source." — same page
- ToS: §5 no "deceptive, unethical, false, or misleading" use; §6 YouTube may "monitor and audit your access ... at any time and without further notice"; §15 "will not ... exceed or circumvent use or quota restrictions"; §24.3 on termination "delete all YouTube API Services (including all API Data)" and certify in writing on request; §8 reasonable security controls. — [YouTube API Services Terms of Service](https://developers.google.com/youtube/terms/api-services-terms-of-service)
- Branding: never combine "YouTube"/"YT" with the app's name (e.g. "YouTube for Kids"); "great app for YouTube" is allowed; logos must link back to YouTube content, appear next to the API feature, not be altered or recoloured, and not be the most prominent element; the YouTube Icon may be used for attribution in icon rows. The branding page does not define a "Sign in with YouTube" button. — [YouTube API Services Branding Guidelines](https://developers.google.com/youtube/terms/branding-guidelines)

**Monetisation: inauthentic / reused content**
- July 15, 2025 notice: "renaming this policy from 'repetitious content' to 'inauthentic content.'" Generic/repetitive not allowed: "Similar or repetitive content with low educational value or minimal variation", "AI-generated content from generic templates that lacks original insight". Reused content not allowed: "Clips of a favorite show edited together with little or no narrative", "short videos compiled from other social media sites", content that gets views "mostly from non-verbal reactions without voice commentary"; allowed: clips for critical review, reaction with commentary, edited footage "where you add a storyline and commentary"; for reused content "monetization may be removed from your entire channel." — [YouTube Help: Channel monetization policies](https://support.google.com/youtube/answer/1311392)
- Secondary: YouTube framed it as "a minor update to our longstanding guideline on repetitious content" and said reaction/clips/commentary channels aren't specifically targeted. — [Search Engine Journal](https://www.searchenginejournal.com/youtube-clarifies-monetization-update-targeting-spam-not-reaction-channels/550755); [ppc.land](https://ppc.land/youtube-clarifies-inauthentic-content-policy-changes/) (secondary)

**Altered or synthetic content disclosure**
- Must disclose content that "Makes a real person appear to say or do something they didn't do", "Alters footage of a real event or place", "Generates a realistic scene that didn't actually occur", or AI music that is the main focus. No disclosure needed for beauty filters, "Color adjustment or lighting filters", background blur, "Caption creation", "Video sharpening, upscaling, or repair", clearly unrealistic content, or production help like scripts/titles/thumbnails. "Disclosing AI content alone won't limit a video's audience or impact its eligibility to earn money." Repeated non-disclosure "may be subject to manual application of a label" and penalties including "removal of content or suspension from the YouTube Partner Program." — [YouTube Help: Disclosing use of altered or synthetic content](https://support.google.com/youtube/answer/14328491)

### Inferences
- "Approve-then-post" is not just a nicety: III.E.3.d and III.I.2 mean every publish, scheduled publish, comment and chat message must be explicitly approved by the creator in advance (a per-clip approve button, or a clearly-worded standing "auto-post approved clips" consent that the creator can revoke). Fully silent auto-posting of AI-picked clips is a policy risk.
- The app must re-pull or delete cached video/analytics data every 30 days and re-check the OAuth grant; keep stats cache TTL at 30 days or less.
- The creator's own gameplay with their own commentary is not "reused content"; the risk is monotonous templated Shorts with no variation, so the app should vary captions/hooks and prefer clips with voice.
- Standard clipping (crop, captions, colour) does not require the synthetic-content flag; only AI voice-over, AI-generated scenes or deepfake-style edits do.

### Gaps
- No doc states numeric quota-audit "triggers" beyond "requesting more than default"; the periodic audit is at YouTube's discretion.
- The "Sign in with YouTube" button artwork/rules are not on the branding page read; Google's generic "Sign in with Google" branding rules apply to the OAuth button (not fetched).

---

## Key question 8: Google OAuth verification for YouTube scopes in 2026

### Takeaway
YouTube scopes are treated as sensitive (not restricted) in Google's docs' own examples, so an external, published app needs brand verification (minutes to 2-3 business days) plus sensitive-scope verification (up to 10 days) with a public homepage, a privacy policy on the same domain, per-scope justifications and an unlisted demo video; until then a Testing app is limited to 100 listed test users whose grants expire after 7 days, and a published-but-unverified app is capped at 100 lifetime users.

### Cited Findings
- Sensitive scopes "require review by Google before any Google Account can grant access"; the doc's example of a sensitive-scope action is "deleting a YouTube video." "The sensitive scope verification process can take up to 10 days to complete." Requirements: publicly accessible home page (not a Play Store/Facebook page); privacy policy "hosted on the same domain as the home page" and linked from the consent screen, disclosing how the app "accesses, uses, stores, and shares Google user data"; per-scope justification why "a narrower scope won't work"; demo video uploaded as Unlisted showing the consent flow in English, app name, OAuth client ID in the address bar and the function each scope enables; domains verified in Search Console. — [Sensitive scope verification](https://developers.google.com/identity/protocols/oauth2/production-readiness/sensitive-scope-verification)
- Restricted scopes "provide wide access to Google user data"; verification "can potentially take several weeks"; security assessment by "Google-empanelled security assessors", reassessed "at least every 12 months"; the page does not list YouTube among restricted scopes and refers to the FAQ for the list. — [Restricted scope verification](https://developers.google.com/identity/protocols/oauth2/production-readiness/restricted-scope-verification)
- FAQ: apps requesting sensitive or restricted scopes "must complete Google's OAuth app verification"; non-sensitive-only apps don't need it; "Apps requesting restricted scopes data need to complete 're-verification' annually"; scope categories "are indicated automatically in the" Cloud Console. — [OAuth App Verification FAQ](https://support.google.com/cloud/answer/9110914)
- Brand verification: needed when External + Published + showing name/logo; automated review "a few minutes", manual "2-3 business days"; "Compliant verification results are valid for 7 days"; Testing apps "only available to users you add to the list of test users", show a tester warning, have a user cap and a limited refresh-token lifetime. — [Brand verification](https://developers.google.com/identity/protocols/oauth2/production-readiness/brand-verification)
- Audience page: Testing apps "are limited to up to 100 test users listed in the OAuth consent screen"; "Authorizations by a test user will expire seven days from the time of consent"; In production apps "are available to any user with a Google Account"; unverified-app user cap is "100 new users in total, after the app presents the unverified app screen", applies "over the entire lifetime of the project, and it cannot be reset or changed", and only counts users granting unapproved sensitive/restricted scopes. — [Google Cloud Help: Configure OAuth audience](https://support.google.com/cloud/answer/15549945)
- Unverified apps: "your app will be limited to 100 new users until it is verified"; "You need to go through verification before you launch a user-facing app"; if the scopes in code differ from the consent-screen config "your users see an 'unverified app' screen". — [Google Cloud Help: Unverified apps](https://support.google.com/cloud/answer/7454865)
- Refresh tokens: an External project in Testing "is issued a refresh token expiring in 7 days" (unless only name/email/profile scopes); "limit of 100 refresh tokens per Google Account per OAuth 2.0 client ID", oldest invalidated silently. — [Google Identity: Using OAuth 2.0](https://developers.google.com/identity/protocols/oauth2)
- Demo video requirements restated on the verification requirements page: "Must show the end-to-end flow of your app including the OAuth grant process" and "the same application you have submitted for verification (including app name, branding)"; restricted scopes add an "annual security assessment". — [Google Cloud Help: Verification requirements](https://support.google.com/cloud/answer/13464321)
- Scopes GCM Clipper needs and their uses per the API docs: `youtube.upload` (insert/thumbnails), `youtube.force-ssl` (captions, comments, live chat insert), `youtube.readonly` (liveBroadcasts.list, videos.getRating since Sept 1, 2026), `yt-analytics.readonly` (Analytics), `yt-analytics-monetary.readonly` (revenue, YPP only). — [videos.insert](https://developers.google.com/youtube/v3/docs/videos/insert); [captions.insert](https://developers.google.com/youtube/v3/docs/captions/insert); [commentThreads.insert](https://developers.google.com/youtube/v3/docs/commentThreads/insert); [liveBroadcasts.list](https://developers.google.com/youtube/v3/live/docs/liveBroadcasts/list); [Channel reports](https://developers.google.com/youtube/analytics/channel_reports)
- Secondary: third-party guides classify all YouTube user-data scopes, including `youtube.upload` and `youtube.readonly`, as sensitive and `youtubepartner` as restricted (CASA Tier 2). — [getphyllo.com](https://www.getphyllo.com/post/youtube-oauth-scopes); [postproxy.dev](https://postproxy.dev/blog/youtube-upload-api-guide/) (secondary; not confirmed on a Google page)

### Inferences
- For the "free tools only" constraint: keep the Cloud project in Testing during development (up to 100 named testers, 7-day re-consent), then publish and submit brand + sensitive-scope verification before any public beta; budget ~2 weeks and a real domain with homepage + privacy policy (free static hosting is fine as long as it is the app's own domain, not a store listing).
- Avoid `youtubepartner` entirely; it is the only YouTube scope with restricted/security-assessment signals, and GCM Clipper does not need it.
- Request the narrowest set: `youtube.upload` + `youtube.force-ssl` + `youtube.readonly` + `yt-analytics.readonly`; the demo video must show each one in use.

### Gaps
- Google's authoritative list classifying each YouTube scope as sensitive vs restricted was not retrieved (the FAQ defers to the Cloud Console's automatic labels); the sensitive classification is inferred from the docs' "deleting a YouTube video" example and secondary guides.
- Typical real-world review time beyond the stated "up to 10 days" could not be sourced from Google.
