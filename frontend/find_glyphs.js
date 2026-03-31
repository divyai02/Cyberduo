const fs = require('fs');
const path = require('path');

function walk(dir, callback) {
    fs.readdirSync(dir).forEach(f => {
        let dirPath = path.join(dir, f);
        let isDirectory = fs.statSync(dirPath).isDirectory();
        isDirectory ? walk(dirPath, callback) : callback(path.join(dir, f));
    });
};

walk('./src', (filePath) => {
    if (filePath.endsWith('.jsx') || filePath.endsWith('.js') || filePath.endsWith('.css')) {
        const content = fs.readFileSync(filePath, 'utf8');
        for (let i = 0; i < content.length; i++) {
            if (content.charCodeAt(i) > 127) {
                console.log(`Non-ASCII at ${filePath} [line ${content.slice(0, i).split('\n').length}]: ${content[i]} (code: ${content.charCodeAt(i)})`);
            }
        }
    }
});
