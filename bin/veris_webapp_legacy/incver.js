const fs = require('fs')

const metaFileName = './assets/meta.json'
const meta = require(metaFileName)

meta.build += 1

fs.writeFile(metaFileName, JSON.stringify(meta), 'utf8', () => console.log(`Updating build number to: ${meta.build}`))