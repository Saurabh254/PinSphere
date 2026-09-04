# 🎨 PinSphere Frontend (Web Client)

The official web client for **PinSphere**—a fast, responsive media discovery and visual curation platform.

---

## 🚀 Key Features & Highlights

- **Dynamic Masonry Grid**: Pinterest-style adaptive multi-column layout with smooth resizing.
- **Progressive Image Loading (Blurhash)**: Canvas-based placeholder rendering decoding compact Blurhash strings to prevent Cumulative Layout Shift (CLS).
- **Semantic Vector Search UI**: Interactive search modal with real-time natural language query dispatch.
- **Rich Media Support**: Tailored playback engines for high-res images, GIFs, audio files (`react-audio-player`), and video (`react-player`).
- **Threaded Comment System**: Nested discussion threads with real-time feedback.
- **Direct-to-S3 Uploads**: Drag-and-drop file dropzone directly streaming binaries to object storage via pre-signed URLs.
- **Authentication**: Seamless Google OAuth 2.0 integration alongside traditional JWT authentication.
- **Theming**: Dark and light mode themes built using Tailwind CSS v4 and DaisyUI.

---

## 🛠️ Tech Stack

- **Framework**: [React 18](https://react.dev/) + [Vite 6](https://vitejs.dev/)
- **Language**: [TypeScript](https://www.typescriptlang.org/) (Strict Mode)
- **Styling**: [Tailwind CSS v4](https://tailwindcss.com/) + [DaisyUI](https://daisyui.com/)
- **Routing**: [React Router v7](https://reactrouter.com/)
- **Icons**: [Remix Icon](https://remixicon.com/) & [Lucide Icons](https://lucide.dev/)
- **State & HTTP**: [Axios](https://axios-http.com/)
- **Image Placeholder**: [Blurhash](https://blurha.sh/) & `react-blurhash`
- **Notifications**: `react-toastify`

---

## 🏁 Getting Started

### Prerequisites
- [Node.js](https://nodejs.org/) (v20+ recommended)
- [npm](https://www.npmjs.com/)

### 1. Install Dependencies
```bash
npm install
```

### 2. Configure Environment
Verify the API endpoint configuration in [`src/constants.tsx`](src/constants.tsx):
```typescript
export const API_URL: string = "http://localhost:8000/api/v1";
```

### 3. Start Development Server
```bash
npm run dev
```
The application will be accessible at `http://localhost:5173/`.

---

## 📦 Available Scripts

| Command | Description |
| :--- | :--- |
| `npm run dev` | Starts the Vite development server with hot module replacement (HMR). |
| `npm run build` | Runs type checks (`tsc -b`) and bundles an optimized production build into `dist/`. |
| `npm run preview` | Previews the production build locally. |
| `npm run type_check` | Runs TypeScript compiler checks across the codebase. |
| `npm run lint` | Runs ESLint with automatic autofixing. |
| `npm run lint_check`| Runs ESLint in check-only mode (used in CI pipeline). |
