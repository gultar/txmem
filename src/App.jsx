import React, { useState, useEffect, useRef, Suspense } from 'react';
import SearchForm from './components/SearchForm';
import Navigation from './components/Navigation';
import SearchResults from './components/SearchResults';
import ActiveText from './components/ActiveText';
const Linguee = React.lazy(() => import('./components/Linguee'));

function App() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState({});
  const [searching, setSearching] = useState(false);
  const [source, setSource] = useState('');
  const [target, setTarget] = useState('');
  const [sourceFilename, setSourceFilename] = useState('');
  const [targetFilename, setTargetFilename] = useState('');
  const [foundSegment, setFoundSegment] = useState('');
  const topOfScreen = useRef(null);
  const highlightedSegmentRef = useRef(null);
  const [scrollToSegment, setScrollToSegment] = useState(false);
  const scrollRef = useRef(null);
  


  const handleSubmit = async (query) => {
    setSearching(true);

    try {
      const response = await fetch(`http://localhost:5000/search?expression=${query}`);
      const data = await response.json();
      const matches = await convertResults(data);

      setResults(matches);
      setQuery(query)
    } catch (error) {
      console.log('Error:', error);
    } finally {
      setSearching(false);
    }
  };

  const convertResults = (data) => {
    return new Promise((resolve) => {
      let matches = {};
      data.results.map((entry) => {
        const [filename, sentence] = entry;
        if (!matches[filename]) {
          matches[filename] = [sentence];
        } else {
          matches[filename].push(sentence);
        }
      });
      resolve(matches);
    });
  };

  const handleFileClick = async (filename, foundSegment) => {
    try {
      filename = filename.replace('#', '%231');
      const response = await fetch(`http://localhost:5000/file?filename=${filename}`);
      const data = await response.json();

      setSource(data['EN'].text);
      setTarget(data['FR'].text);
      setSourceFilename(data['EN'].filename)
      setTargetFilename(data['FR'].filename)
      setFoundSegment(foundSegment);
      setScrollToSegment(true);
    } catch (error) {
      console.log('Error:', error);
    }
  };

  useEffect(() => {
    if (scrollToSegment && scrollRef.current) {
      setTimeout(()=>{
        // window.scrollTo(0, scrollRef.current.offsetTop); 
        scrollRef.current.scrollIntoView({
          block: 'center',
          inline: 'nearest',
          behavior: 'smooth'
        });
        setScrollToSegment(false);
      }, 100)
    }
  }, [scrollToSegment]);

  return (
    <div className="main" ref={topOfScreen}>
      <Navigation onSubmit={handleSubmit} searching={searching} />

      
      <div className="test-block"></div>
      <div className="deepl-block"></div>
      <div className="display-output">
          <SearchResults results={results} onFileClick={handleFileClick} />

          <ActiveText 
            source={source} 
            target={target} 
            foundSegment={foundSegment} 
            scrollRef={scrollRef}
            src_filename={sourceFilename}
            target_filename={targetFilename} />
          <Suspense fallback={<div>Loading Linguee component...</div>}>
            <Linguee query={query} />
          </Suspense>
      </div>
    </div>
  );
}

export default App;
