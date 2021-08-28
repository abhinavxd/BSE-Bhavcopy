import React, { useState, Suspense } from "react";
import { render } from "react-dom";
import axios from "axios";
import "../css/homepage.css";
import "react-awesome-button/dist/styles.css";
import { CSVLink } from "react-csv";
import Autocomplete from '@material-ui/lab/Autocomplete';
import TextField from '@material-ui/core/TextField';
const DataTable = React.lazy(() => import('react-data-table-component'));


const Homepage = () => {
    const [searchedData, setSearchedData] = useState([]);
    const [csvData, setCsvData] = useState(undefined);
    const [currentStockName, setCurrentStockName] = useState("default");
    const columns = [
        {
            name: 'DATE',
            selector: 'DATE',
            sortable: true,
        },
        {
            name: 'SC_NAME',
            selector: 'SC_NAME',
            sortable: false
        },
        {
            name: 'SC_CODE',
            selector: 'SC_CODE',
            sortable: false
        },
        {
            name: 'OPEN',
            selector: 'OPEN',
            sortable: false
        },
        {
            name: 'HIGH',
            selector: 'HIGH',
            sortable: false
        },
        {
            name: 'LOW',
            selector: 'LOW',
            sortable: false
        },
        {
            name: 'CLOSE',
            selector: 'CLOSE',
            sortable: false,
        },
    ];

    const handleInputChange = async (e) => {
        const searchTerm = e.target.value;
        const result = await axios.post('api/search-prefix', {
            search_term: searchTerm
        });
        setSearchedData(result.data)
    };

    const handleSearch = async (e, value = undefined) => {
        e.preventDefault();
        try {
            const result = await axios.post("api/get-data-by-name", {
                sc_name: value.title
            });
            if (result.status === 200) {
                setCsvData(result.data.data)
                setCurrentStockName(result.data.name)
            }
        } catch (err) {
            setCsvData(undefined);
        }
    };

    return (
        <>
            <div className="container">
                <h2>
                    Welcome to <img src="https://www.bseindia.com/include/images/bselogo.png" /> (Equity) Bhavcopy Search
                </h2>
                <div>
                    <form id='search-form' onSubmit={(e) => e.preventDefault()}>
                        <Autocomplete
                            id="search-input"
                            onChange={(event, value) => handleSearch(event, value)}
                            options={searchedData}
                            getOptionLabel={(option) => option.title}
                            style={{ width: 400 }}
                            renderInput={(params) => <TextField {...params} label="Search by name" variant="outlined" onChange={handleInputChange} />}
                        />
                    </form>
                </div>
                <div>
                    {csvData && <CSVLink filename={`bhavcopy_equity_${currentStockName}.csv`} data={csvData}><i className="fa fa-download" aria-hidden="true"></i>Download CSV</CSVLink>}
                </div>
                {csvData &&
                    <div className='data-table'>
                        <Suspense fallback={<div>Loading...</div>}>
                            <DataTable
                                title=''
                                columns={columns}
                                data={csvData}
                            />
                        </Suspense>
                    </div>
                }
            </div>
        </>
    )
};
export default Homepage;

const container = document.getElementById("app");
render(<Homepage />, container);