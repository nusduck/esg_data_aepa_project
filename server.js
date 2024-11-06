const express = require('express');
const multer = require('multer');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
const cors = require('cors');

const app = express();
const port = 3002;

// Enable CORS
app.use(cors());

// Set up storage for multer
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, path.join(__dirname, 'data/esg_reports_pdf'));
  },
  filename: (req, file, cb) => {
    cb(null, file.originalname);
  },
});

// Set up file filter for multer
const fileFilter = (req, file, cb) => {
  const filePath = path.join(__dirname, 'data/esg_reports_pdf', file.originalname);
  if (fs.existsSync(filePath)) {
    // If file exists, skip saving
    req.fileAlreadyExists = true;
    cb(null, false);
  } else {
    cb(null, true);
  }
};

const upload = multer({ storage, fileFilter });

// Endpoint to handle file upload
app.post('/upload', upload.single('file'), (req, res) => {
  if (req.fileAlreadyExists) {
    return res.send({ message: 'File already exists, upload skipped', fileUrl});
  }

  if (!req.file) {
    return res.status(400).send({ message: 'No file uploaded' });
  }

  const fileUrl = `http://localhost:${port}/uploads/${req.file.filename}`;
  res.send({ message: 'File uploaded successfully', fileUrl });
});


app.get('/run-python', (req, res) => {
    const scriptPath = path.join(__dirname, 'scripts', 'your_script.py');
    exec(`python ${scriptPath}`, (error, stdout, stderr) => {
      if (error) {
        console.error(`Error executing script: ${error.message}`);
        return res.status(500).send(`Error executing script: ${error.message}`);
      }
      if (stderr) {
        console.error(`Script error: ${stderr}`);
        return res.status(500).send(`Script error: ${stderr}`);
      }
      res.send(stdout);
    });
});

app.get('/read-file', (req, res) => {
    const filePath = path.join(__dirname, req.query.path);
    // console.log(filePath);
    fs.readFile(filePath, 'utf8', (err, data) => {
      if (err) {
        console.error(`Error reading file: ${err.message}`);
        return res.status(500).send(`Error reading file: ${err.message}`);
      }
      res.send(data);
    });
});  

// Endpoint to get the list of companies (file names)
app.get('/companies', (req, res) => {
  const directoryPath = path.join(__dirname, 'data/esg_reports_pdf');
  fs.readdir(directoryPath, (err, files) => {
    if (err) {
      return res.status(500).send({ message: 'Unable to scan files' });
    }
    // Extract file names without extensions and '_report'
    files = files.map((file) => {
      return file.replace('_report.pdf', '');
    });
    res.send(files);
  });
});

// Serve static files from the uploads directory
app.use('/uploads', express.static(path.join(__dirname, 'data/esg_reports_pdf')));


app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});