import React, { useEffect, useState } from 'react';

function Linguee({ query }) {
  const [data, setData] = useState(null);
  const [translations, setTranslations] = useState([]);
  const [externalSources, setExternalSources] = useState(null);
  const apiUrl = `http://localhost:5000/linguee?query=${encodeURIComponent(query)}`;

  useEffect(() => {
      if (query !== '') {
      const fetchData = async () => {
          try {
            const response = await fetch(apiUrl);
            const jsonData = await response.json();
            setExternalSources(jsonData.external_sources);
            console.log(jsonData.external_sources)
            if(jsonData.translations && jsonData.translations.length > 0){
                let translations = []
                jsonData.translations.map(unit =>{
                    translations = [translations, ...unit.translations]
                })
                setTranslations(translations);
                console.log('translations',translations)
            }
            
          
          } catch (error) {
          console.error('Error:', error);
          }
      };

      fetchData();
      }
  }, [apiUrl, query]);

  return (
    <div className="linguee ui-element">
        <h3 className='section-header'>Linguee</h3>
        <div className="translation-section">
            <h5>Suggestion de traduction: </h5>
            {
                (
                    translations && Object.keys(translations).length > 0 ? translations.map(
                        tr => {
                            return <><h4>{tr.text}</h4></>
                        }) : ""
                )
            }
        </div>
        {
            (query !='' ?
                externalSources ? (
                    externalSources.map((entry, index) => (
                    <div key={index} className="linguee-example-line">
                        <div className="src">
                            
                            <p>{entry.src}
                                <caption className="linguee-link">
                                    <a href={entry.src_url}>{entry.src_url}</a>
                                </caption>
                            </p>
                        </div>
                        <div className="dst">
                            
                            <p>
                                {entry.dst}
                                <caption className="linguee-link">
                                    <a href={entry.dst_url}>{entry.dst_url}</a>
                                </caption>
                            </p>    
                        </div>
                    </div>
                    ))
                ) : (
                    <p>Loading data...</p>
                )
                :
                <></>
            )
        }
    </div>
  );
}

export default Linguee;
