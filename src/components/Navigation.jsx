import React from 'react';
import SearchForm from './SearchForm';

function Navigation({ onSubmit, searching }) {
    
    return (
      <div className="nav-container">
        <div className="nav">
            <SearchForm onSubmit={onSubmit}/>
            {searching && <div className="search-message">Searching...</div>}
        </div>
      </div>
    );
  }
  
  export default Navigation;