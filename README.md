<h1>Setup</h1>
<details>
   <summary>Click to see Setup instructions</summary>
  <ul>
  <li>Replace <a href=https://github.com/Ghostboy00/imguploader/blob/master/host.py#L8>this</a> with your domain.</li>
  <li>Generate a secure master key and insert it into <a href="https://github.com/Ghostboy00/imguploader/blob/master/endpoints/methods.py#L16">methods.py</a> </li>
  <li>Enter your webhooks in <a href="https://github.com/Ghostboy00/imguploader/blob/master/endpoints/methods.py#L14#L15">methods.py</a></li>
  <li>Fill in your website icon, name and embed description in
  <a href="https://github.com/Ghostboy00/imguploader/blob/master/endpoints/methods.py#L17#L19">methods.py</a></li>
  <br>
  <br>
  <li>Copy the ShareX config from below and enter your domain.</li>
  <li>Open ShareX -> Destinations -> Custom uploader settings...</li>
<details>
   <summary>Click to see image</summary>
  <img src="https://i.ibb.co/09jpjDJ/image.png">
</details>
  <li>Click on Import->From Clipboard</li>
  <br>
<details>
   <summary>Click to see image</summary>
  <img src="https://i.ibb.co/dBkpv0p/image.png">
</details>
 <li>Have fun :)</li>
  </ul>
</details>
<h1>Endpoints</h1>
<details>
   <summary>Click to see all available endpoints</summary>
<ul>
  <li>Keymanagement endpoints (These endpoints must contain master_key in the payload | GET requests):
    <ul>
      <li>https://example.com/deletekey This endpoint allows you to delete a key.</li>
      <li>https://example.com/reset This endpoint allows you to reset a key.</li>
      <li>https://example.com/fetchkeys This endpoint allows you to fetch a list of available keys.</li>
      <li>https://example.com/createkey This endpoint allows you to create a new key.</li>
      <li>https://example.com/config This endpoint lets you modify the embed color, webhook (log), and embed text</li>
    </ul>
  </li>
  <li>Public endpoints:
    <ul>
      <li>https://example.com/upload This endpoint allows you to upload an image.</li>
      <li>https://example.com/<:imagename:> This endpoint allows you to retrieve an image with the specified name.</li>
    </ul>
  </li>
</ul>
</details>





<h1>ShareX Config</h1>


```json
{
  "Version": "14.1.0",
  "Name": "https://yourdomain.com/upload",
  "DestinationType": "ImageUploader, FileUploader",
  "RequestMethod": "POST",
  "RequestURL": "https://yourdomain.com/upload",
  "Parameters": {
    "api_key": ""
  },
  "Body": "MultipartFormData",
  "FileFormName": "image",
  "URL": "{response}"
}
```
