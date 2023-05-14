import cloudinary
import cloudinary.api
import cloudinary.uploader

# Set up your Cloudinary credentials
cloudinary.config(
  cloud_name = 'drqnkfexf',
  api_key = '127479953536276',
  api_secret = 'w-r7AP5-XtCykP61KxvWKfNr7y8'
)
# The Cloudinary folder to list files from
folder_name = "audios"

# Initialize empty lists for the URLs and durations
urls = []
durations = []

# Use the Cloudinary API to list all files in the folder
try:
    response = cloudinary.api.resources(type='upload', prefix=folder_name, max_results=500)
    files = response['resources']
    for file in files:
        # Check if the file is an audio file
        if file["resource_type"] == "video":
            continue
        else:
            # Retrieve the URL of the audio file
            url = cloudinary.utils.cloudinary_url(file["public_id"], resource_type=file["resource_type"])[0]

            # Retrieve the duration of the audio file
            duration = file["duration"]

            # Append the URL and duration to the respective lists
            urls.append(url)
            durations.append(duration)

    # Check if there are more files to list
    while 'next_cursor' in response:
        response = cloudinary.api.resources(type='upload', prefix=folder_name, max_results=500, next_cursor=response['next_cursor'])
        files = response['resources']
        for file in files:
            # Check if the file is an audio file
            if file["resource_type"] == "video":
                continue
            else:
                # Retrieve the URL of the audio file
                url = cloudinary.utils.cloudinary_url(file["public_id"], resource_type=file["resource_type"])[0]

                # Retrieve the duration of the audio file
                duration = file["duration"]

                # Append the URL and duration to the respective lists
                urls.append(url)
                durations.append(duration)

except cloudinary.api.Error as e:
    print("Cloudinary API Error:", e.message)

# Print the list of URLs and durations
print("URLs: " + str(urls))
print("Durations: " + str(durations))
