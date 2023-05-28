import React from 'react';

function SearchResults({ results, onFileClick }) {
    const maxCharsDisplayed = 100
  
  const handleFileClick = (filename, sentence) => {
    filename = filename.replace('#', '%231');
    
    onFileClick(filename, sentence);
  };

  return (
    <div className="segments">
        <h2 className='section-header'>Files</h2>
      {Object.keys(results).map((filename) => (
        <ul className="match-filename" key={filename}>
          <strong>{filename}</strong>
          {results[filename].map((sentence) => (
            <a className="match-segment" href="#" onClick={() => handleFileClick(filename, sentence)}>
              <li key={sentence}>o  {(sentence.length <=maxCharsDisplayed?sentence:sentence.slice(0, maxCharsDisplayed)+"...")}</li>
            </a>
          ))}
        </ul>
      ))}
    </div>
  );
}

export default SearchResults;
