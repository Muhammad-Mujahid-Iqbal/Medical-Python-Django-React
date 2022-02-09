import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import Table from 'react-bootstrap/Table';
import Button from 'react-bootstrap/Button';
import React, { useState, useEffect } from 'react';
function App() {
  const [responseData, setData] = useState([]);
  const [selectedFile, setSelectedFile] = useState();
  const [isFilePicked, setIsSelected] = useState(false);
  useEffect(() => {
    fetchRecotd();
  }, []);
  const changeHandler = (event) => {
    setSelectedFile(event.target.files[0]);
    setIsSelected(true);
  }
  const handleSubmission = () => {
    const formData = new FormData();
    formData.append('File', selectedFile);
    fetch(
      'http://localhost:8000/api/patients/',
      {
        method: 'POST',
        body: formData,
      }
    )
      .then((result) => {
        console.log(result.status)
        if (result.status==200){
          setIsSelected(false);
          fetchRecotd();
          setSelectedFile('');
          alert('Data inserted successfully.');
        }
        else{
          alert('Something went wrong.Kindly check data format/duplication.');
        }
      })
      .catch((error) => {
        alert('Something went wrong.Kindly check data format/duplication.');
      });
  }; 
const fetchRecotd = () => {
  fetch('http://localhost:8000/api/patients/')
    .then(response => {
      return response.json();
    }).then(result => {
      setData(result);
    });
}
return (
  <div className="App">
    <div className="header"><h4>Medical</h4></div>
    <div className="body">
      <input type="file" name="file" onChange={changeHandler} />
      {isFilePicked &&
      <Button onClick={handleSubmission} className="mb-3 mt-0">Upload Users</Button>
      }
      <Table striped bordered hover responsive>
        <thead>
          <tr>
            <th>#</th>
            <th>First Name</th>
            <th>Last Name</th>
            <th>Visit Reasons</th>
          </tr>
        </thead>
        <tbody>
          {responseData && responseData.map((value, index) => {
            return <tr key={index}>
              <td>{index + 1}</td>
              <td>{value.first_name}</td>
              <td>{value.last_name}</td>
              <td>
                <ul>
                  {value.visits.map((value2, index2) => {
                    return <li key={`${index2}-${index}`}>{value2.reason} - {value2.visit_date}</li>
                  })}
                </ul>
              </td>
            </tr>
          })}
        </tbody>
      </Table>
    </div>
  </div>
);
}
export default App;