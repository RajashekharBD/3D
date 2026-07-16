
# Frontend Architecture

## Overview

The frontend provides a clean, responsive, and interactive interface for users to upload an image, monitor AI processing, preview outputs, visualize the generated 3D model, and download all generated assets.

The frontend is built using:

- Next.js 15
- React 19
- TypeScript
- Tailwind CSS
- React Three Fiber
- Drei
- Three.js

---

# Frontend Goals

The application should:

- Be simple to use
- Be responsive
- Display real-time pipeline progress
- Visualize generated GLB models
- Preview generated images
- Allow downloading all outputs
- Handle errors gracefully

---

# User Workflow

```
Home

↓

Upload Image

↓

Image Preview

↓

Upload

↓

Pipeline Processing

↓

Progress Screen

↓

Results Screen

↓

3D Viewer

↓

Download Files
```

---

# Application Structure

```
frontend/

app/

components/

hooks/

services/

types/

utils/

public/
```

---

# Pages

## Home

Route

```
/
```

Purpose

Landing page.

Components

- Hero
- Features
- Start Button

---

## Upload

Route

```
/upload
```

Purpose

Upload image.

Components

- Drag & Drop Area
- File Picker
- Image Preview
- Upload Button

---

## Processing

Route

```
/processing/[jobId]
```

Purpose

Display processing progress.

Components

- Progress Bar
- Current Stage
- Estimated Time
- Status Message

---

## Results

Route

```
/results/[jobId]
```

Purpose

Display generated outputs.

Components

- Detection Image
- Segmentation Image
- RGBA Image
- 3D Viewer
- Download Buttons

---

# Layout

```
Navbar

↓

Main Content

↓

Footer
```

---

# Navbar

Contains

- Logo
- Home
- Upload
- About

---

# Footer

Contains

- Copyright
- Version
- GitHub
- Documentation

---

# Components

## Upload Component

Purpose

Select image.

Features

- Drag & Drop
- File Picker
- Preview
- Validation

---

## Image Preview

Shows

Original Image

---

## Progress Component

Displays

Progress Bar

Current Stage

Remaining Time

Status

---

## Result Card

Displays

Generated Image

Download Button

---

## Download Panel

Contains

Download buttons for

- GLB
- Point Cloud
- Detection Image
- Segmentation Image
- RGBA Image
- Metadata

---

## 3D Viewer

Technology

React Three Fiber

Purpose

Display GLB

Features

- Orbit Controls
- Zoom
- Rotate
- Pan
- Auto Fit
- Reset Camera

---

# State Management

React State

Stores

- Uploaded Image
- Job ID
- Progress
- Status
- Output URLs
- Errors

---

# API Communication

Upload

↓

Receive Job ID

↓

Poll Status

↓

Completed

↓

Load Results

---

# Progress Stages

```
0%

Uploading

↓

10%

Image Analysis

↓

20%

CLAHE

↓

30%

Caption Generation

↓

45%

Object Detection

↓

60%

Segmentation

↓

70%

Background Removal

↓

80%

3D Generation

↓

95%

Point Cloud

↓

100%

Completed
```

---

# File Validation

Allowed

- JPG
- JPEG
- PNG
- WEBP
- BMP

Maximum Size

25 MB

Validation

- File Type
- File Size
- Image Readability

---

# Error Handling

Upload Error

↓

Show Error Message

↓

Retry

---

Pipeline Error

↓

Display Failed Stage

↓

Retry Button

---

Download Error

↓

Retry Download

---

# Loading Indicators

Upload

↓

Spinner

↓

Progress Bar

↓

Completed Badge

---

# Responsive Design

Supported Devices

Desktop

Laptop

Tablet

Mobile

---

# Theme

Primary

Blue

Secondary

Gray

Success

Green

Error

Red

Warning

Yellow

---

# Typography

Headings

Bold

Body

Regular

Buttons

Medium

---

# Accessibility

- Keyboard Navigation
- Screen Reader Support
- High Contrast
- Visible Focus States
- Alt Text for Images

---

# Performance

- Lazy Loading
- Image Optimization
- Dynamic Imports
- Code Splitting
- GLB Lazy Loading

---

# Security

- Validate File Type
- Validate File Size
- Sanitize File Name
- Prevent Multiple Uploads

---

# Folder Structure

```
components/

Upload/

Progress/

Viewer/

Results/

Download/

Navbar/

Footer/

Common/
```

---

# User Journey

```
Open Website

↓

Upload Image

↓

Preview

↓

Start Processing

↓

Watch Progress

↓

View Results

↓

Inspect 3D Model

↓

Download Files
```

---

# Future Enhancements

- Dark Mode
- Batch Upload
- Drag-and-Drop Multiple Files
- Compare Original vs Generated
- Full-Screen 3D Viewer
- Measurement Tools
- Share Results
- Project History
- User Accounts
