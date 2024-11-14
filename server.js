const express = require('express');
const multer = require('multer');
const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');
const { spawn } = require('child_process');
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
  // Check if file was uploaded or if it already exists
  if (req.fileAlreadyExists) {
    const fileUrl = `http://localhost:${port}/uploads/${req.file?.filename}`;
    return res.send({ message: 'File already exists, upload skipped', fileUrl });
  }

  if (!req.fileAlreadyExists) {
    const fileUrl = `http://localhost:${port}/uploads/${req.file?.filename}`;
    return res.send({ message: 'This is a new file', fileUrl });
  }

  if (!req.file) {
    return res.status(400).send({ message: 'No file uploaded' });
  }

  // If a new file was successfully uploaded
  const fileUrl = `http://localhost:${port}/uploads/${req.file.filename}`;
  res.send({ message: 'File uploaded successfully', fileUrl });
  console.log(fileUrl);
});

// run main.py, start analysis
app.get('/start-analysis', (req, res) => {
  console.log('Starting analysis...', req.query.file);
  const fileName = req.query.file;

  const pythonProcess = spawn('python3', ['src/main.py', fileName]);

  let dataString = '';

  // console.log('company:', company)
  pythonProcess.stdout.on('data', (data) => {
    dataString += data.toString();
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  pythonProcess.on('close', (code) => {
    if (code !== 0) {
      return res.status(500).send({ message: 'Error processing analysis!' });
    }
    const results = JSON.parse(dataString);
    // console.log(results);
    res.json(results);
  });

  


})


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


// Endpoint to get the score data from CSV files
app.get('/score-data', (req, res) => {
  const directoryPath = path.join(__dirname, 'data/esg_scores');
  const company = req.query.company;

  const pythonProcess = spawn('python3', ['src/datafetch/get_score.py', directoryPath, company]);

  let dataString = '';

  // console.log('company:', company)
  pythonProcess.stdout.on('data', (data) => {
    dataString += data.toString();
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  pythonProcess.on('close', (code) => {
    if (code !== 0) {
      return res.status(500).send({ message: 'Error processing CSV files' });
    }
    const results = JSON.parse(dataString);
    // console.log(results);
    res.json(results);
  });

  
});


// Endpoint to get the metrics data from json files
app.get('/company-metrics', (req, res) => {
  const directoryPath = path.join(__dirname, 'data/esg_scores/extracted_esg_data.json');
  const company = req.query.company;

  const pythonProcess = spawn('python3', ['src/datafetch/get_value.py', directoryPath, company]);

  let dataString = '';

  console.log('company:', company)
  pythonProcess.stdout.on('data', (data) => {
    dataString += data.toString();
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  pythonProcess.on('close', (code) => {
    if (code !== 0) {
      return res.status(500).send({ message: 'Error processing CSV files' });
    }
    const results = JSON.parse(dataString);
    // console.log(results);
    res.json(results);
  });

  
});

// Endpoint to get the realtime data from json files
app.get('/realtime-data', (req, res) => {
  const directoryPath = path.join(__dirname, 'data/esg_realtime_info/esg_realtime_info_obtain.json');
  const company = req.query.company;

  const pythonProcess = spawn('python3', ['src/datafetch/get_realtime.py', directoryPath, company]);

  let dataString = '';

  pythonProcess.stdout.on('data', (data) => {
    dataString += data.toString();
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  pythonProcess.on('close', (code) => {
    if (code !== 0) {
      return res.status(500).send({ message: 'Error processing json files' });
    }
    const results = JSON.parse(dataString);
    // console.log(results);
    res.json(results);
  });
});


// Endpoint to get the greenwash data from json files
app.get('/greenwash-data', (req, res) => {
  const directoryPath = path.join(__dirname, 'data/esg_green_wash/greenwashing_analysis_result.json');
  const company = req.query.company;
  const pythonProcess = spawn('python3', ['src/datafetch/get_greenwash.py', directoryPath, company]);

  let dataString = '';

  pythonProcess.stdout.on('data', (data) => {
    dataString += data.toString();
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  pythonProcess.on('close', (code) => {
    if (code !== 0) {
      return res.status(500).send({ message: 'Error processing JSON files' });
    }

    try {
      //console.log('green_wash_data', dataString);
      const results = JSON.parse(dataString); 
      res.json(results); 
    } catch (error) {
      console.error('JSON parsing error:', error);
      res.status(500).send({ message: 'Failed to parse JSON output' });
    }
  });
});

// Endpoint to get the validation data from json files
app.get('/validation-company', (req, res) => {
  const directoryPath = path.join(__dirname, 'data/esg_validation/shown_final_score_of_retrieve.csv');
  const company = req.query.company;
  const pythonProcess = spawn('python3', ['src/datafetch/get_validation.py', directoryPath]);

  let dataString = '';

  pythonProcess.stdout.on('data', (data) => {
    dataString += data.toString();
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  pythonProcess.on('close', (code) => {
    if (code !== 0) {
      return res.status(500).send({ message: 'Error processing JSON files' });
    }

    try {
      console.log('validation_data', dataString);
      const results = JSON.parse(dataString); 
      res.json(results); 
    } catch (error) {
      console.error('JSON parsing error:', error);
      res.status(500).send({ message: 'Failed to parse JSON output' });
    }
  });
});

// Serve static files from the uploads directory
app.use('/uploads', express.static(path.join(__dirname, 'data/esg_reports_pdf')));


app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});