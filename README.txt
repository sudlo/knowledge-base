## How to get Knowledge Base.exe

1. Create a free account at https://github.com if you do not have one

2. Create a new repository
   - Click the + icon top right → New repository
   - Name it: knowledge-base
   - Set it to Private
   - Click Create repository

3. Upload these two files into the repository
   - app.py
   - .github/workflows/build.yml
   (drag and drop them into the GitHub web interface)

4. GitHub automatically starts building

5. Wait about 3 minutes

6. Go to the Actions tab in your repository
   - Click the latest workflow run
   - Under Artifacts, download "Knowledge Base"
   - Inside the zip is Knowledge Base.exe

7. That exe is your product
   - No Python needed on customer machines
   - No install needed
   - Double-click and it runs on any Windows 10 or 11 PC

Every time you push a change to app.py, GitHub rebuilds the exe automatically.
The latest exe also appears under the Releases tab of your repository.
