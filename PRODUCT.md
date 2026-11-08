# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Independent filmmakers and small film teams managing a production.

## Product Purpose

The Open Filmmaker Toolkit provides practical tools for filmmakers' production workflows. Success means completing and preserving useful production records locally.

## Positioning

The tools work offline with a shared `.oft.json` project file, keeping project information on the user's computer.

## Operating Context

Users open individual tools in a browser, work with a shared project file, and save or export records when needed. Opening the project file on the home page shows a dashboard of what needs attention across the tools. Teams share the file through a folder their sync app keeps in step; the tools warn when someone else has it open and merge copies, without any server.

## Capabilities and Constraints

Tools are single-file HTML applications with no dependencies or network requests. Code several tools need lives in `shared/` and is copied into each page, so each stays a single file. They must preserve project fields and collections they do not own. The Archive log records copies, storage locations, hash manifests supplied by the user, and manually recorded read-back checks; it does not send background reminders or compute media hashes.

## Product Principles

- Keep project data local.
- Preserve the shared project file.
- Support practical production work without requiring accounts or network access.

## Accessibility & Inclusion

Tools must be keyboard accessible, label their fields, work at phone width, and support dark mode.
