<!DOCTYPE html>

<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Random Images Page with Text</title>
<style>
    body {
      font-family: Arial, sans-serif;
      text-align: center;
      padding: 20px;
      background-color: #f0f0f0;
    }
    h1 {
      color: #333;
    }
    p {
      color: #555;
      font-size: 1.1em;
      max-width: 800px;
      margin: 0 auto 20px;
    }
    .image-container {
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 20px;
      margin: 30px 0;
    }
    .image-container img {
      width: 300px;
      height: 200px;
      object-fit: cover;
      border-radius: 12px;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
  </style>
</head>
<body>
<h1>Explore Random Images</h1>
<p>Welcome to our gallery of random images! Each time you visit this page, you’ll see a fresh collection of beautiful and unpredictable visuals pulled from the web. Enjoy the surprise and let your imagination roam.</p>
<div class="image-container">
<img alt="Random Image 1" src="images\image_0.png"/>
<img alt="Random Image 2" src="images\image_1.png"/>
<img alt="Random Image 3" src="images\image_2.png"/>
<img alt="Random Image 4" src="images\image_3.png"/>
<img alt="Random Image 5" src="images\image_4.png"/>
</div>
<p>We hope you found these images inspiring! Whether you're looking for creative ideas, a moment of beauty, or just something fun to look at, come back again for more randomness!</p>
</body>
</html>
