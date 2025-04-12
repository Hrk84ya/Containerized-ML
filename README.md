# 🏠 Containerized Machine Learning: House Price Predictor
Welcome to the Containerized Machine Learning: House Price Predictor project! 
This application leverages a trained machine learning model to predict house prices based on input features. The entire application is containerized using Docker, ensuring seamless deployment and scalability.

## 📦 Project Overview
This project demonstrates the integration of machine learning with DevOps practices. It includes:
  - Model Training: A script to train the machine learning model using historical housing data.
  - API Development: A Flask-based API to serve predictions.
  - Containerization: Dockerization of the application for consistent deployment across environments.
  - CI/CD Integration: GitHub Actions workflows and Jenkins for automated testing and deployment.

## 🚀 Getting Started

**Prerequisites** <br>
	-	[Docker](https://www.docker.com/products/docker-desktop/) <br>
	-	[Git](https://git-scm.com/downloads) <br>
 	- 	[Jenkins](https://www.jenkins.io/download/)

**Installation**
1. Clone the Repository
   ```bash
   git clone https://github.com/Hrk84ya/Containerized-ML.git
   cd Containerized-ML
   ```
2. Build the Docker Image
   ```bash
   docker build -t house-price-predictor .
   ```
3. Run the Docker container
   ```bash
   docker run -d -p 5050:5050 house-price-predictor
   ```
4. Access the API <br>
   Navigate to http://localhost:5050 to interact with the API.

## 🧠 Model Training

The train_model.py script is used to train the machine learning model. It processes the dataset, trains the model, and saves it as model.pkl.

To train the model:
```bash
python train_model.py
```
Ensure that the dataset is placed in the appropriate directory and the script is configured with the correct path.

## 🖥️ API Usage

The Flask API exposes an endpoint to predict house prices.
  - Endpoint: /predict
  - Method: POST
  - Payload:
    ```json
    {
    "feature1": value1,
    "feature2": value2,
    ...
    }
    ```
  - Response:
    ```json
    {
    "predicted_price": value
    }
    ```
Replace feature1, feature2, etc., with the actual feature names used in your model.

## 🛠️ Project Structure
- app.py: Flask application to serve the model
- train_model.py: Script to train and save the machine learning model
- test_app.py: Used to check response code of the server
- model.pkl: Serialized trained model
- requirements.txt: Python dependencies
- Dockerfile: Instructions to build the Docker image
- Jenkinsfile: Instructions for CI/CD Pipeline
- .github/workflows/ci-cd.yml: GitHub Actions workflow for CI/CD

## 🔄 Continuous Integration & Deployment
The project utilizes both GitHub Actions and Jenkins for CI/CD. These tools automate the process of testing, building, and deploying the application.

### GitHub Actions

The workflow defined in .github/workflows/ci-cd.yml automates the following:
- Linting and testing the codebase
- Building the Docker image
- Deploying the Docker container

This ensures that every change is tested and deployed seamlessly within the GitHub ecosystem.

### Jenkins

A Jenkinsfile is included in the repository to support Jenkins-based CI/CD. Jenkins executes a similar pipeline:
- Checking out the source code
- Building the Docker image
- Running tests
- Deploying the container
- Post Action Steps

This setup provides flexibility to run CI/CD pipelines either through GitHub Actions or within a Jenkins-managed environment, depending on your deployment preferences.

## ⚙️ Jenkins Integration

Jenkins is also configured in this project to automate the CI/CD pipeline. A Jenkinsfile defines the stages involved in building, testing, and deploying the application inside a Jenkins environment.

Jenkins Pipeline Stages:
- Checkout: Pulls the latest code from the GitHub repository
- Setup: Python Environment is established and requirements are downloaded
- Test: Runs tests to validate the application logic and the virtual environment as well
- Build: Constructs the Docker image from the provided Dockerfile
- Deploy: Deploys the containerized application to the target environment (if on main branch)
- Post Actions: Success/Failure Message for the pipeline

To run the Jenkins pipeline:
1. Ensure Jenkins is installed and running.
2. Install necessary plugins (e.g., Docker, Pipeline).
3. Create a new pipeline job and connect it to the repository.
4. Jenkins will automatically detect the Jenkinsfile and execute the defined stages.

This integration provides an alternative to GitHub Actions and allows for more customizable and extensible CI/CD pipelines.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository) file for details.

## 🙌 Acknowledgements
  - [Scikit-learn](https://scikit-learn.org/) for machine learning algorithms.
  - [Flask](https://flask.palletsprojects.com/en/stable/) for the web framework.
  - [Docker](https://www.docker.com/) for containerization.
  - [Jenkins](https://www.jenkins.io/) for CI/CD
  - [GitHub Actions](https://github.com/features/actions) for CI/CD.

