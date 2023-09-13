import React from 'react';
import Tokenizer from './Tokenizer';

function ActiveText({ source, target, foundSegment, scrollRef, src_filename, target_filename }) {
    console.log(foundSegment, scrollRef, src_filename, target_filename)
  return (
    
    <div className="active-text ui-element">
        
      <div className="source">
        <h3>{src_filename}</h3>
        <Tokenizer text={source} foundSegment={foundSegment} scrollRef={scrollRef} />
      </div>
      <div className="target">
        <h3>{target_filename}</h3>
        <Tokenizer text={target} foundSegment={""} scrollRef={null} />
      </div>
    </div>
  );
}

export default ActiveText;
