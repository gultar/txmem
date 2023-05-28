const fs = require('fs');

async function readJsonFile(filePath) {
  try {
    const data = await fs.promises.readFile(filePath, 'utf8');
    const obj = JSON.parse(data);
    console.log(obj['./fac\\220616-002e Indigenous Declaration Edits\\220616-002e Indigenous Declaration Edits.docx']["FR"].text)
  } catch (err) {
    console.error(err);
  }
}

// Replace 'path/to/your/file.json' with the path to your JSON file
readJsonFile('./memory.json');
