# Motion Detection for CCTV Cameras App

This project is a real-world application developed using Django, SQLite, and OpenCV. The goal of the project is to implement smart motion-based frame removal techniques in a responsive website, optimizing storage requirements for CCTV cameras.

## Features

- Smart motion detection algorithm using OpenCV to identify and extract frames with motion.
- Responsive web interface to view and manage the CCTV camera footage.
- Automatic frame removal based on motion detection to optimize storage space.
- User-friendly dashboard to configure camera settings and view motion alerts.
- Secure user authentication and access control.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/LeandrAnders0n/motion-based-frame-removal
```

2. Navigate to the project directory:

```bash
cd motion-detection-cctv
```

3. Create and activate a virtual environment (optional but recommended):

```bash
python3 -m venv venv
source venv/bin/activate
```

4. Install the required packages:

```bash
pip install -r requirements.txt
```

5. Apply database migrations:

```bash
python manage.py migrate
```

6. Start the development server:

```bash
python manage.py runserver
```

7. Access the application in your web browser at `http://localhost:8000`.

## Usage

1. Register a new account or log in to an existing account.
2. Add CCTV cameras to the system and configure their settings.
3. Access the live camera feed and view the motion alerts.
4. Navigate through the intuitive interface to manage and monitor the CCTV cameras.
5. Customize the motion detection algorithm and frame removal settings as per your requirements.

## Contributing

Contributions to this project are welcome. To contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make the necessary changes and commit your code.
4. Push your changes to your forked repository.
5. Submit a pull request to the main repository.

Please ensure that your code follows the project's coding style and conventions.

