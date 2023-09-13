import React from 'react';

function Tokenizer({ text, foundSegment, scrollRef }) {
  text = text.replace("M.","Monsieur")
  text = text.replace("Monsieur","M.")
  const splitTextIntoSentences = (text) => {
    const regex = /(?<!^M\. [A-Z])(?<!\w\.\w.)(?<!\b(?:Mme|Mlle)(?!\.))(?<!\b(?:Mr|Mrs|Ms|Dr|M)\.)(?<![A-Z]\.-[A-Z]\.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!|\;|\☒|\☐|\.\”)(?!\s*»)(?!\.[A-Z]\.)(\s|(?<=^|\s)M\.\s[A-Z]\..*)/;
    const sentences = text.split(regex);
    return sentences;
  };

  
  const selectClasses = (segment, foundSegment) => {
    return (segment === foundSegment ? 'sentence-match sentence' : 'sentence');
  }

  const sentences = splitTextIntoSentences(text);
  
  return sentences
    .filter(segment => segment.trim() !== '') // Filter out empty segments
    .map((segment, index) => (
      <p
        key={index} // It's recommended to add a unique key when mapping over elements
        className={selectClasses(segment, foundSegment)}
        ref={(segment === foundSegment ? scrollRef : null)}
      >
        {segment}
      </p>
    ));
}

export default Tokenizer;
