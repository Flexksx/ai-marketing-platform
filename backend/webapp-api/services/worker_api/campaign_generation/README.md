# Campaign Generation Worker

## Overview

The Campaign Generation Worker is responsible for orchestrating the complete lifecycle of campaign creation in Voisso. It processes campaign generation jobs through 4 sequential phases, each building upon the previous results to create a complete campaign with generated posts ready for scheduling.

## Job Lifecycle

Campaign generation jobs follow this state machine:

```
PENDING → IN_PROGRESS → COMPLETED
              ↓
            FAILED
```

- **PENDING**: Job created, waiting for worker processing
- **IN_PROGRESS**: Currently being processed through the 4 phases
- **COMPLETED**: All phases successfully completed
- **FAILED**: An error occurred during processing

## Processing Flow

The campaign generation workflow consists of 4 sequential phases, orchestrated by `CampaignGenerationJobProcessingService`:

### Phase 1: Campaign Description Generation

**File**: `steps/campaign_description.py`
**Step**: `CampaignDescriptionGenerationStep`

Generates the foundational campaign strategy and metadata using AI.

**Input**:
- Brand data (name, mission, archetype, tone of voice, audience, etc.)
- User's campaign idea/input

**Process**:
1. Fetch brand details
2. Create AI prompt combining brand context and user input
3. Call OpenAI GPT-5-Mini with structured output format
4. Parse and validate `CampaignGenerationDescriptionResult`

**Output** (`CampaignGenerationDescriptionResult`):
- `name`: Campaign name
- `goal`: Campaign objective
- `description`: Detailed campaign description
- `target_audience`: Target audience description
- `content_pillar`: Primary content theme
- `start_date`: Campaign start date
- `duration_days`: Campaign duration
- `channels`: List of channels (INSTAGRAM, LINKEDIN)

**Updates**: `job.result.description_result`

---

### Phase 2: Image Addition

**File**: `steps/image_addition.py`
**Step**: `CampaignImageAdditionGenerationStep`

Ensures the campaign has sufficient visual assets by generating AI images if needed.

**Input**:
- Existing campaign images from user (`job.image_urls`)
- Brand data and campaign description

**Process**:
1. Check if image count meets minimum threshold (10 images)
2. If insufficient:
   - Generate AI images using NanoBanana/Gemini service
   - Upload images to Supabase Storage
3. Combine user-provided and AI-generated images

**Output**:
- Updated `image_urls` list with at least 10 images

**Updates**: `job.result.image_urls`

**External Services**:
- AI Image Generation (Gemini)
- Supabase Storage (image hosting)

---

### Phase 3: Posting Plan Generation

**File**: `steps/posting_plan.py`
**Step**: `CampaignPostingPlanGenerationStep`

Creates a detailed posting schedule for the campaign duration.

**Input**:
- Campaign description result
- Campaign duration and channels
- Brand context

**Process**:
1. Calculate campaign start date (2 days from today)
2. Create AI prompt with campaign details
3. Call OpenAI to generate structured posting plan
4. Parse `CampaignGenerationPostingPlanResult`

**Output** (`CampaignGenerationPostingPlanResult`):
```python
{
    "plan_items": [
        {
            "channel": PostChannel,           # INSTAGRAM or LINKEDIN
            "description": str,                # What the post should be about
            "scheduled_at": datetime,          # When to publish
            "post_generation_job_id": None     # Populated in Phase 4
        },
        ...
    ]
}
```

**Updates**: `job.result.posting_plan_result`

**Notes**:
- Each plan item describes a post to be created
- Images are distributed round-robin across posts
- `post_generation_job_id` is initially `None`, populated in Phase 4

---

### Phase 4: Post Generation

**File**: `steps/post_generation.py`
**Step**: `PostGenerationCampaignGenerationStep`

Creates individual post generation jobs for each posting plan item and processes them asynchronously.

**Input**:
- Posting plan result with plan items
- Campaign images

**Process**:
1. For each posting plan item:
   - Assign an image (round-robin selection)
   - Create `PostGenerationJob` via `PostGenerationJobService`
   - Store job ID back into `plan_item.post_generation_job_id`
2. Process all post generation jobs concurrently using `asyncio.gather`
3. Wait for all posts to complete

**Output**:
- Each posting plan item now has `post_generation_job_id` populated
- Individual post generation jobs are created and processed
- Generated captions are stored in each `PostGenerationJob.result`

**Updates**: `posting_plan_result.plan_items[*].post_generation_job_id`

**Key Relationship**:
```
CampaignGenerationJob
  └─> posting_plan_result
       └─> plan_items[]
            ├─> description
            ├─> channel
            ├─> scheduled_at
            └─> post_generation_job_id  ← Links to PostGenerationJob
```

**See Also**: `backend/services/worker_api/post_generation/README.md`

---

## Data Flow

```
User Input + Brand Data
         ↓
┌─────────────────────────────────────────────┐
│ Phase 1: Campaign Description               │
│ → name, goal, target_audience, etc.         │
└─────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────┐
│ Phase 2: Image Addition                     │
│ → image_urls[] (minimum 10 images)          │
└─────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────┐
│ Phase 3: Posting Plan Generation            │
│ → plan_items[] with descriptions & schedule │
└─────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────┐
│ Phase 4: Post Generation                    │
│ → post_generation_job_id for each plan item │
└─────────────────────────────────────────────┘
         ↓
    Completed Campaign
```

## Data Models

### CampaignGenerationJobResult

The main result object that accumulates data through all phases:

```python
class CampaignGenerationJobResult(BaseModel):
    description_result: Optional[CampaignGenerationDescriptionResult] = None
    image_urls: List[str] = []
    posting_plan_result: Optional[CampaignGenerationPostingPlanResult] = None
```

**Phase Updates**:
- Phase 1 → `description_result`
- Phase 2 → `image_urls`
- Phase 3 → `posting_plan_result`
- Phase 4 → `posting_plan_result.plan_items[*].post_generation_job_id`

### CampaignGenerationPostingPlanItem

```python
class CampaignGenerationPostingPlanItem(BaseModel):
    channel: PostChannel
    description: str
    scheduled_at: datetime
    post_generation_job_id: Optional[str] = None
```

The `post_generation_job_id` is the key link between campaign generation and post generation:
- Initially `None` after Phase 3
- Populated during Phase 4
- Used by UI to fetch generated post captions

## Error Handling

If any phase fails:
1. Exception is caught by `CampaignGenerationJobProcessingService.process()`
2. Job status is set to `FAILED`
3. `result` and `image_urls` are cleared
4. Error is logged and re-raised

Error handling is fail-fast: if a phase fails, subsequent phases are not executed.

## Integration

### Cloud Tasks

Campaign generation is triggered via Cloud Tasks:
1. Client API creates job via `/campaign-creation` endpoint
2. Cloud Tasks enqueues job processing
3. Worker API receives task and calls `CampaignGenerationJobProcessingService.process()`

### Database

After each phase:
- Job is updated in database via `CampaignGenerationJobService.update()`
- Status changes from `PENDING` → `IN_PROGRESS` → `COMPLETED`
- `result` field is progressively populated

### Related Services

- **Brand Service**: Fetches brand data for context
- **OpenAI Service**: Generates campaign description and posting plans
- **AI Image Generation**: Generates images via Gemini/NanoBanana
- **Supabase Storage**: Hosts campaign images
- **Post Generation Service**: Creates and processes individual post jobs

## Dependencies

Campaign generation steps are wired together in `worker_api/dependencies.py`:

```python
def get_campaign_job_processor(
    campaign_service: CampaignGenerationJobService,
    openai_service: AsyncOpenAIService,
    supabase_service: SupabaseStorageService,
    brand_service: BrandService,
    post_generation_service: PostGenerationJobService,
) -> CampaignGenerationJobProcessingService
```

## Usage Example

```python
processor = get_campaign_job_processor(...)
result = await processor.process(job_id="uuid", user_id="user-uuid")
```

After completion, the campaign has:
- Complete campaign description
- 10+ curated images
- Detailed posting schedule
- Generated post captions (accessible via post_generation_job_id)

