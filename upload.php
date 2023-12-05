<?php
    session_start();

    $servername = "localhost";
    $databaseName = "database_name";
    $username = "username";
    $password = "password";

    $connection = new mysqli($servername, $username, $password, $databaseName);

    if (!$connection) {
        die("Connection failed: " . $connection->connect_error);
    }

    $uploadDirectory = 'uploads/';
    $uploadedFile = $uploadDirectory . basename($_FILES['image']['name']);

    if (move_uploaded_file($_FILES['image']['tmp_name'], $uploadedFile)) {
        echo "File is valid, and was successfully uploaded.";
    } else {
        echo "Upload failed";
    }

    $fileName = basename($_FILES['image']['name']);

    $insertQuery = "INSERT INTO images (file_name) VALUES ('$fileName')";
    $mysqli->query($insertQuery);
?>