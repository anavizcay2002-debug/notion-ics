# Notion Calendar Sync — Apple app

This folder contains the shared SwiftUI/WidgetKit source for the future iPhone and macOS app.

## Targets

Create an Xcode project with:

- `NotionCalendarSync` — iOS app
- `NotionCalendarSyncMac` — macOS app
- `NotionCalendarSyncWidget` — Widget Extension with iOS + macOS support

The shared status client reads:

`https://anavizcay2002-debug.github.io/notion-ics/status.json`

The calendar feed is:

`https://anavizcay2002-debug.github.io/notion-ics/calendar.ics`

## Design

The app and widget should show sync status, last update time, event count and the five-minute refresh interval. Manual refresh will be added through a secure server-side action rather than embedding a GitHub token in the app.
