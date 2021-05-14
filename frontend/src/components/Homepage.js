import React, { useState, useEffect } from "react";
import { render } from "react-dom";
import axios from "axios";
import swal from 'sweetalert';
import "../css/homepage.css";
import { AwesomeButton } from "react-awesome-button";
import "react-awesome-button/dist/styles.css";
import { CSVLink } from "react-csv";
import DataTable from 'react-data-table-component';
import 'react-toastify/dist/ReactToastify.css';
import { ToastContainer, toast } from 'react-toastify';

const Homepage = () => {
    const [searchTerm, setSearchTerm] = useState('');
    const [csvData, setCsvData] = useState(undefined);
    const [error, setError] = useState(false);
    const columns = [
        {
            name: 'SC_NAME',
            selector: 'SC_NAME',
            sortable: true,
        },
        {
            name: 'SC_CODE',
            selector: 'SC_CODE',
            sortable: true,
            right: true,
        },
        {
            name: 'OPEN',
            selector: 'OPEN',
            sortable: true,
            right: true,
        },
        {
            name: 'HIGH',
            selector: 'HIGH',
            sortable: true,
            right: true,
        },
        {
            name: 'LOW',
            selector: 'LOW',
            sortable: true,
            right: true,
        },
        {
            name: 'CLOSE',
            selector: 'CLOSE',
            sortable: true,
            right: true,
        },
    ];

    const handleInputChange = (e) => {
        setSearchTerm(e.target.value);
    };

    const clearTable = () => {
        setCsvData(undefined);
    }

    const handleSearch = async (e) => {
        e.preventDefault();
        if (searchTerm.length == 0) {
            return;
        }
        setError(false);
        try {
            const result = await axios.post("api/get-data-by-name", {
                sc_name: searchTerm
            });
            if (result.status === 200) {
                setCsvData(result.data)
            }
        } catch (err) {
            setError(true);
            setCsvData(undefined);
            swal({
                icon: "error",
                title: "Name not found"
            });
        }
    };

    return (
        <>
            <div className="container">
                <h1>
                    Welcome to <img src="https://www.bseindia.com/include/images/bselogo.png" /> Bhavcopy (Equity) downloader
                </h1>
                <div>
                    <form onSubmit={handleSearch} id='search-form'>
                        <label>Search by name (case insensitive)</label>
                        <input type="text" onChange={handleInputChange} id='search-input' />
                        <AwesomeButton type="primary">Search</AwesomeButton>
                    </form>
                </div>
                <div>
                    {csvData && <CSVLink data={csvData}><i className="fa fa-download" aria-hidden="true"></i>Download CSV</CSVLink>}
                </div>
                {csvData && <span id="pro-tip">PRO TIP: Click on column names to sort data in ascending order or descending order</span>}
                {csvData &&
                    <div className='data-table'>
                        <DataTable
                            title="BSE Bhavcopy (Equity)"
                            columns={columns}
                            data={csvData}
                        />
                    </div>
                }
            </div>
        </>
    )
};
export default Homepage;

const container = document.getElementById("app");
render(<Homepage />, container);