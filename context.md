# Conference Management System Microservices Architecture

This document details the microservices architecture of the conference management system, including services, interfaces, data flows, and communication patterns.

## System Overview

The system is a microservice-based application for managing conferences, with web and mobile clients. It follows a modern architecture with an API Gateway pattern, service-to-service communication, and event-driven analytics.

## Microservices Components

### Frontend Clients
- **WebApp**: Browser-based client interface
  - Methods: `interactWithApi()`
- **MobileApp**: Mobile application interface
  - Methods: `interactWithApi()`
- Both clients communicate with the backend exclusively through the API Gateway

### Core Services

#### API Gateway
- **Primary Responsibilities**:
  - Route client requests to appropriate microservices
  - Validate authentication tokens
  - Aggregate results from multiple services
  - Publish events to the event bus
- **Endpoints**: Serves as the single entry point for all client requests
- **Data**: Primarily passes data between clients and services without persistent storage
- **Key Methods**: `routeRequest()`, `validateAuthToken()`, `aggregateResults()`

#### Auth Service
- **Primary Responsibilities**:
  - Authenticate users
  - Validate auth tokens
  - Refresh tokens
- **Interfaces**: Implements `IAuthService`
- **Data**: User credentials, authentication tokens
- **Events**: Publishes login and Monthly Active Users (MAU) events to analytics
- **Key Methods**: `authenticate()`, `validateToken()`, `refreshToken()`

#### User Profile Service
- **Primary Responsibilities**:
  - Retrieve user profiles
  - Update user profile information
- **Interfaces**: Implements `IUserProfileService`
- **Data**: User profile information (names, preferences, etc.)
- **Key Methods**: `getUserProfile()`, `updateUserProfile()`

### Conference Services

#### Conference Metadata Service
- **Primary Responsibilities**:
  - List available conferences
  - Provide conference details
  - Add new conferences
  - Update conference information
  - Store conference endpoint information
- **Interfaces**: Implements `IConferenceMetadata`
- **Data**: Conference metadata (titles, dates, locations, endpoints)
- **Events**: Publishes events to analytics
- **Admin Integration**: Receives conference management commands from Admin Service
- **Key Methods**: `listConferences()`, `getConferenceDetails()`, `addConference()`, `updateConference()`, `findConferenceEndpoint()`

#### Conference Data Service
- **Primary Responsibilities**:
  - Provide conference schedules
  - List content items (talks, sessions, etc.)
  - Provide detailed content information
  - List authors/speakers
  - Provide room information
- **Interfaces**: Implements `IConferenceData`
- **Data**: 
  - Conference schedules
  - Content items details
  - Room information
  - Speaker/author information
- **Storage**: Utilizes conference-specific databases
- **Events**: Publishes data access events to analytics
- **Key Methods**: `getSchedule()`, `listContentItems()`, `getContentItemDetails()`, `getRooms()`, `listAuthors()`

### User Services

#### User Notes Service
- **Primary Responsibilities**:
  - Create user notes
  - Retrieve notes for specific users
  - Retrieve notes for specific content items
  - Update notes
  - Delete notes
- **Interfaces**: Implements `IUserNotes`
- **Data**: User notes linked to conferences and content items
- **Events**: Publishes note interaction events to analytics
- **Key Methods**: `createNote()`, `getNotesForUser()`, `getNotesForItem()`, `updateNote()`, `deleteNote()`

### Admin & Analytics

#### Admin Service
- **Primary Responsibilities**:
  - Trigger addition of new conferences
  - Trigger updates to conferences
  - View system analytics
  - Manage conference provisioning workflow
- **Dependencies**: 
  - `IConferenceMetadata` (for conference management)
  - `IAnalytics` (for viewing analytics data)
- **Data**: Admin configuration, provisioning status
- **Key Methods**: `triggerAddConference()`, `triggerUpdateConference()`, `viewSystemAnalytics()`

#### Analytics Service
- **Primary Responsibilities**:
  - Record engagement events
  - Provide Monthly Active Users (MAU) metrics
  - Provide conference access statistics
- **Interfaces**: Implements `IAnalytics`
- **Data**: User engagement metrics, access patterns, usage statistics
- **Event Consumption**: Subscribes to all system events via the Event Bus
- **Key Methods**: `recordEngagementEvent()`, `getMonthlyActiveUsers()`, `getConferenceAccessStats()`

### Infrastructure Components

#### Event Bus
- **Purpose**: Decouples event producers from consumers
- **Primary Responsibilities**: 
  - Routes events from producers to consumers
  - Ensures reliable delivery of events
- **Event Types**: 
  - User activity events
  - Data access events
  - Login/MAU events
  - Note interaction events
- **Key Methods**: `publishEvent()`, `subscribeToEvents()`

## Interfaces

- **IAuthService**: `authenticate()`, `validateToken()`, `refreshToken()`
- **IUserProfileService**: `getUserProfile()`, `updateUserProfile()`
- **IConferenceMetadata**: `listConferences()`, `getConferenceDetails()`, `addConference()`, `updateConference()`, `findConferenceEndpoint()`
- **IConferenceData**: `getSchedule()`, `listContentItems()`, `getContentItemDetails()`, `listAuthors()`, `getRoomInfo()`
- **IUserNotes**: `createNote()`, `getNotesForUser()`, `getNotesForItem()`, `updateNote()`, `deleteNote()`
- **IAnalytics**: `recordEngagementEvent()`, `getMonthlyActiveUsers()`, `getConferenceAccessStats()`

## Communication Patterns

### Synchronous Communication
1. Clients → API Gateway: HTTPS requests
2. API Gateway → Various Services: Direct service-to-service calls
3. Admin Service → Conference Metadata Service: Conference management commands

### Asynchronous Communication
1. Various Services → Event Bus: Publishing events
2. Event Bus → Analytics Service: Delivering events for processing

## Key Processes

### Standard User Flow
1. User requests data via Frontend
2. Frontend sends request to API Gateway
3. API Gateway validates token with Auth Service
4. API Gateway retrieves conference info from Metadata Service
5. API Gateway requests specific data from Conference Data Service
6. API Gateway may request/manage notes via User Notes Service
7. API Gateway returns aggregated response to Frontend
8. API Gateway publishes events to Event Bus for analytics

> **Note:** This flow is an example based on the sequence diagram for retrieving a conference schedule. Other flows may follow similar patterns.

### Adding a New Conference (Admin)
1. Admin logs in and submits conference details
2. Admin Service validates input
3. On valid input, Admin Service calls Metadata Service to save conference info
4. **Provisioning process** creates database and deploys service (distinct actor/process)
5. Endpoint is registered back in Metadata Service
6. Admin is notified of success/failure

## Data Ownership
Each microservice owns and is responsible for its own data domain:
- Auth Service: Authentication data
- User Profile Service: User profile data
- Conference Metadata Service: Conference metadata
- Conference Data Service: Conference content and schedule data
- User Notes Service: User notes
- Analytics Service: System metrics and analytics data
