<h1 align="center">
  MoeWalls API
</h1>
<p align="center">
  MoeWalls API is a Flask-based web service that allows users to search for and retrieve wallpapers from the MoeWalls website.
</p>
<p align="center">
    <a href="https://discord.gg/your-discord-invite">
      <img src="https://img.shields.io/discord/1220631055845822485?color=7289da&label=discord&logo=discord&logoColor=7289da" alt="Discord">
    </a>
    <a href="https://github.com/zuhaz/moewalls-api/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/zuhaz/moewalls-api" alt="GitHub">
  </a>
</p>

MoeWalls API provides an easy way to integrate MoeWalls content into your applications.

#### IMPORTANT
> This API is not officially affiliated with MoeWalls. It is a third-party API that scrapes publicly available data from the MoeWalls website. Please use responsibly and in accordance with MoeWalls' terms of service.

**Disclaimer:** The developers of this API are not responsible for any misuse, damage, or legal issues that may arise from using this service. Users are solely responsible for ensuring their use of this API complies with all applicable laws and terms of service.

<h2> Table of Contents </h2>

- [Features](#features)
- [Installation](#installation)
  - [Local Deployment](#local-deployment)
  - [Deploy to Vercel (Recommended)](#deploy-to-vercel-recommended)
- [Usage (Locally/Server)](#usage-locallyserver)
- [API Documentation](#api-documentation)
- [Development](#development)
- [License](#license)
- [Support](#support)

## Features

- Search for wallpapers by keyword
- Retrieve wallpaper details including title, URL, thumbnail, and video URL
- Pagination support for search results
- Caching to improve performance and reduce load on the MoeWalls website
- CORS support for cross-origin requests
- Gzip compression for API responses

## Installation

### Local Deployment

1. Clone the repository:
   ```
   git clone https://github.com/zuhaz/moewalls-api.git
   cd moewalls-api
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Linux or MacOS
   venv\Scripts\activate  # On Windows
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the project root (or rename the existing `.env.example` file) and add the following:
   ```
   FLASK_DEBUG=False
   FLASK_HOST=127.0.0.1
   FLASK_PORT=5000
   ```
   Adjust these values as needed for your deployment environment.

### Deploy to Vercel (Recommended)

You can deploy this project to Vercel with one click:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/zuhaz/moewalls-api)

## Usage (Locally/Server)

To run the API server:
```
python main.py
```

The server will start on the host and port specified in your `.env` file.

## API Documentation

### Endpoints

#### 1. Search Wallpapers

- **URL:** `/api/search`
- **Method:** GET
- **Parameters:**
  - `q` (required): Search term
  - `page` (optional, default: 1): Page number
  - `limit` (optional): Number of wallpapers to return per page
- **Response:** JSON object containing search results

Example:
```
GET /api/search?q=cat&page=1&limit=10
```

#### 2. Get Total Pages

- **URL:** `/api/total_pages`
- **Method:** GET
- **Parameters:**
  - `q` (required): Search term
- **Response:** JSON object containing the total number of pages

Example:
```
GET /api/total_pages?q=cat
```

## Development

To run the server in debug mode, set `FLASK_DEBUG=True` in your `.env` file.

## License

This project is licensed under the [MIT License](LICENSE).

## Support

If you need help or have any questions, please [open an issue](https://github.com/zuhaz/moewalls-api/issues) or join our [Discord server](https://discord.gg/7mhdvfgybX).

<a style="display: flex; justify-content: center;" href="https://discord.gg/7mhdvfgybX">
   <img src="https://discordapp.com/api/guilds/1220631055845822485/widget.png?style=banner2"/>
</a>
