# ZennVid
ZennVid is a full-stack platform for generating, processing, and serving multimedia content — video, audio, and text — using advanced AI/ML capabilities.

## Features
* User authentication and authorization
* Video generation using AI models (SadTalker and Magic Video)
* Feed management with likes and comments
* API key management
* Translation, audio generation, and caption generation
* Payment processing using Razorpay
* Credit updates and transaction management
* Video saving and retrieval
* Email sending using Nodemailer

## Tech Stack
| Technology | Description |
| --- | --- |
| PyTorch | Machine learning framework |
| Express | Web framework for Node.js |
| Python | Programming language |
| Next.js | React framework for building server-side rendered applications |
| Node.js | JavaScript runtime environment |
| JSON | Data interchange format |
| Axios | HTTP client library |
| MongoDB | NoSQL database |
| Whisper | Automatic speech recognition system |
| React | JavaScript library for building user interfaces |
| TanStack React Query | Data fetching and caching library |
| Zod | Schema validation library |
| TensorFlow | Machine learning framework |
| Nodemailer | Email sending library |
| Cloudinary | Cloud-based media management platform |
| Express.js | Web framework for Node.js |
| Mongoose | MongoDB object modeling tool |
| TypeScript | Programming language |
| JavaScript | Programming language |
| Razorpay | Payment gateway |
| Groq | AI model serving platform |

## Architecture
The ZennVid platform follows a microservices architecture, with separate modules for authentication, video generation, feed management, and API management. The platform uses a combination of machine learning frameworks, including PyTorch and TensorFlow, to generate videos using AI models. The frontend is built using Next.js and React, while the backend is built using Express.js and Node.js.
```mermaid
graph LR
    A[User] -->|auth|> B(Authentication)
    B -->|success|> C(Dashboard)
    C -->|video request|> D(Video Generation)
    D -->|video generated|> E(Video Saving)
    E -->|video saved|> F(API Management)
    F -->|API key|> G(Developer Portal)
```
Unfortunately, no rendered diagram images are available.

## Getting Started
### Prerequisites
* Node.js installed on your system
* MongoDB installed and running on your system
* Python installed on your system
* PyTorch and TensorFlow installed on your system

### Installation Steps
1. Clone the repository using `git clone https://github.com/Devan019/ZennVid.git`
2. Install dependencies using `npm install` or `yarn install`
3. Set up MongoDB and connect to the database using the MongoDB Node.js driver
4. Configure environment variables and API keys
5. Start the Express server using `node api-server.js`
6. Start the Next.js frontend using `npm run dev` or `yarn dev`

### Environment Setup
* Set up a MongoDB database and connect to it using the MongoDB Node.js driver
* Configure Cloudinary and Razorpay APIs
* Set up environment variables for the API server and frontend

### Running the Project
* Start the Express server using `node api-server.js`
* Start the Next.js frontend using `npm run dev` or `yarn dev`

## Project Structure
```markdown
├── ai-service/
│   ├── apis/
│   │   ├── classes/
│   │   │   └── pydentic_class.py
│   │   ├── helpers/
│   │   │   ├── coqui/
│   │   │   │   ├── audios/
│   │   │   │   └── voice_cloning.py
│   │   │   ├── sadtaker/
│   │   │   │   └── lip_sync.py
│   │   │   ├── test-media/
│   │   │   │   ├── test.srt
│   │   │   │   └── test2.srt
│   │   │   ├── assembia_captaions.py
│   │   │   ├── edge_tts.py
│   │   │   ├── ffmepg.py
│   │   │   ├── functions.py
│   │   │   ├── gemini_image_gen.py
│   │   │   ├── gemini_script.py
│   │   │   ├── gen_video.py
│   │   │   ├── groq_script.py
│   │   │   ├── test_uploader.py
│   │   │   ├── translate.py
│   │   │   └── wisper_model.py
│   │   ├── api.py
│   │   ├── requirements.txt
│   │   └── v2_api.py
│   ├── openapi/
│   │   ├── api.py
│   │   ├── audio_gen.py
│   │   ├── requirements.txt
│   │   ├── translate.py
│   │   └── wisper_model.py
│   ├── .gitignore
│   └── SadTalker
├── api-server/
│   ├── src/
│   │   ├── api/
│   │   │   ├── Admin/
│   │   │   │   ├── analisys/
│   │   │   │   └── user/
│   │   │   ├── feed/
│   │   │   │   ├── controller.ts
│   │   │   │   ├── feed.ts
│   │   │   │   ├── route.ts
│   │   │   │   ├── schema.ts
│   │   │   │   └── service.ts
│   │   │   ├── openapi/
│   │   │   │   ├── api/
│   │   │   │   ├── controller.ts
│   │   │   │   ├── key-template.ts
│   │   │   │   ├── model.ts
│   │   │   │   └── schema.ts
│   │   │   ├── pricing/
│   │   │   │   ├── controller.ts
│   │   │   │   ├── model.ts
│   │   │   │   └── schema.ts
│   │   │   ├── video_generater/
│   │   │   │   ├── models/
│   │   │   │   ├── controller.ts
│   │   │   │   ├── schema.ts
│   │   │   │   └── service.ts
│   │   │   ├── videoapi/
│   │   │   │   └── controller.ts
│   │   │   └── route.ts
│   │   ├── auth/
│   │   │   ├── model/
│   │   │   │   ├── tmpUser.ts
│   │   │   │   └── User.ts
│   │   │   ├── schema/
│   │   │   │   └── zodschema.ts
│   │   │   ├── controller.ts
│   │   │   ├── route.ts
│   │   │   └── service.ts
│   │   ├── constants/
│   │   │   ├── common.ts
│   │   │   ├── interfaces.ts
│   │   │   └── provider.ts
│   │   ├── oauth/
│   │   │   ├── controller.ts
│   │   │   ├── route.ts
│   │   │   └── service.ts
│   │   ├── script/
│   │   │   ├── addApps.ts
│   │   │   ├── addTranscations.ts
│   │   │   ├── addusers.ts
│   │   │   ├── addVideos.ts
│   │   │   ├── route.ts
│   │   │   └── updateFeed.ts
│   │   ├── test/
│   │   │   ├── audio.json
│   │   │   └── route.ts
│   │   ├── types/
│   │   │   └── Request.ts
│   │   ├── utils/
│   │   │   ├── cloudinary.ts
│   │   │   ├── cyrpto.ts
│   │   │   ├── expressAsync.ts
│   │   │   ├── ExpressError.ts
│   │   │   ├── formateResponse.ts
│   │   │   ├── getTodayDate.ts
│   │   │   ├── jwtAssign.ts
│   │   │   ├── mongoConnection.ts
│   │   │   ├── OptGenerater.ts
│   │   │   ├── passwordCompare.ts
│   │   │   ├── redisClient.ts
│   │   │   ├── SendMail.ts
│   │   │   ├── setCookie.ts
│   │   │   └── Voicemappping.ts
│   │   ├── env_var.ts
│   │   ├── middleware.ts
│   │   └── server.ts
│   ├── .gitignore
│   ├── nodemon.json
│   ├── package-lock.json
│   ├── package.json
│   └── tsconfig.json
```
The key directories and files are:
* `ai-service/`: contains the AI model serving code
* `api-server/`: contains the Express.js server code
* `web-client/`: contains the Next.js frontend code
* `api-server/src/api/`: contains the API endpoint code
* `api-server/src/auth/`: contains the authentication code
* `api-server/src/utils/`: contains utility functions

## Usage
To use the ZennVid platform, follow these steps:
1. Start the Express server using `node api-server.js`
2. Start the Next.js frontend using `npm run dev` or `yarn dev`
3. Open a web browser and navigate to `http://localhost:3000`
4. Log in to the platform using your credentials
5. Navigate to the dashboard and click on the "Generate Video" button
6. Select the video type and enter the required details
7. Click on the "Generate" button to generate the video

## API
The ZennVid platform provides the following API endpoints:
* `POST /api/auth/otp`: sends an OTP to the user's email or phone number
* `POST /api/auth/verify-otp`: verifies the OTP entered by the user
* `POST /api/video`: generates a video using the AI model
* `GET /api/videos`: retrieves a list of generated videos
* `POST /api/videos/:id/share`: shares a generated video on social media

## Contributing
To contribute to the ZennVid platform, follow these steps:
1. Fork the repository using `git fork https://github.com/Devan019/ZennVid.git`
2. Clone the forked repository using `git clone https://github.com/your-username/ZennVid.git`
3. Create a new branch using `git branch your-branch-name`
4. Make changes to the code and commit them using `git commit -m "your-commit-message"`
5. Push the changes to the remote repository using `git push origin your-branch-name`
6. Create a pull request to merge the changes into the main repository

## License
The ZennVid platform is licensed under the MIT License.