# FORTUNA FLOW - WEB

| ![Gambar 1](/docs/images/home.png) | ![Gambar 2](/docs/images/transactions.png) | ![Gambar 3](/docs/images/report.png) | ![Gambar 4](/docs/images/profile.png) |
| :--------------------------------: | :----------------------------------------: | :----------------------------------: | :-----------------------------------: |

Front-end of [fortuna-flow](/README.md).

## Table of Contents

- [FORTUNA FLOW - WEB](#fortuna-flow---web)
  - [Table of Contents](#table-of-contents)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Building](#building)
  - [Contributing](#contributing)

## Requirements

- Node JS v20.10.0
- NPM v10.2.3

## Installation

Steps to install this project.

1. Clone this repository
   ```bash
   git clone https://github.com/Shiyinq/fortuna-flow.git
   ```
2. Navigate to the project directory:
   ```bash
   cd fortuna-flow/frontend
   ```
3. Install dependencies:
   ```bash
   npm install
   ```
4. Make `.env` file
   ```bash
   cp .env.example .env
   ```

## Usage

Once you've clone a repository and installed dependencies with `npm install` (or `pnpm install` or `yarn`), start a development server:

```bash
npm run dev

# or start the server and open the app in a new browser tab
npm run dev -- --open
```

NOTE: Please ensure that you run the backend API first. You can find instructions in the [README](/README.md) file.

## Building

To create a production version of your app:

```bash
npm run build
```

You can preview the production build with `npm run preview`.

> To deploy your app, you may need to install an [adapter](https://kit.svelte.dev/docs/adapters) for your target environment.

## Contributing

- You can open [issues](https://github.com/Shiyinq/quest-by-system/issues) to report bugs or request features.
- You can fix bugs and add features on your own.
  1. Fork this repository
  2. Create a feature branch `git checkout -b new-feature`
  3. Commit your changes `git commit -m 'Add new feature'`
  4. Push to the branch `git push origin new-feature`
  5. Create a Pull Request
