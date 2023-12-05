!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Penpal Image Upload</title>
        <style>
            body {
                font-family: Arial, Helvetica, sans-serif;
                text-align: center;
                margin: 20px;
            }
        </style>
    </head>
    <body>
        <h1>Penpal Image Upload</h1>

        <form action="upload.php" enctype="multipart/form-data">
            <label for="imageInput">Select a file:</label>
            <input type="file" id="imageInput" name="image" accept="image/*" required">
            <br>
            <input type="submit" value="upload">
        </form>

        <?php
            $selectQuery = "SELECT * FROM images";
            $result = $mysqli->query($selectQuery);
        
            while ($row = $result->fetch_assoc()) {
                echo "<img src='uploads/{$row['file_name']} alt='Image' style='margin-top: 20px;'>";
            }
        ?>
    </body>
</html>
