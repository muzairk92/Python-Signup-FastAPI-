  import React, { useState, useEffect } from 'react';
  import axios from 'axios';
  import TextField from '@mui/material/TextField';
  import Button from '@mui/material/Button';
  import Container from '@mui/material/Container';
  import Cookies from 'universal-cookie';


  const SignupForm = () => {
    const [formData, setFormData] = useState({
      name: '',
      email: '',
      password: '',
      csrf_token: '', // Include csrf_token in your form state
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
      const fetchCsrfToken = async () => {
        try {
          const response = await axios.get('http://127.0.0.1:8000/get_csrf_token', { withCredentials: true });
          
        
          setFormData((prevData) => ({ ...prevData, csrf_token: response.data.csrf_token }));

          // Manually set the cookie (not recommended for CSRF tokens)
          // Cookies.set('csrf_token', response.data.csrf_token, { expires: 1, path: '' });

          const cookies = new Cookies();
          cookies.set( 'csrf_token', response.data.csrf_token, { path: '/' });
          console.log('CSRF Token fetched2:', cookies.get(response.data.csrf_token,)); // Pacman
          
        } catch (error) {
          console.error('Error fetching CSRF token:', error);
        }
      };
    
      fetchCsrfToken();
    }, []);


    // const handleChange = (e) => {
    //   console.log('Before Submit:', formData);
    //   setFormData({
    //     ...formData,
    //     [e.target.name]: e.target.value,
    //   });
    //   console.log('After Submit:', formData);
    // };

    const handleChange = (e) => {
      // Use the callback form to log the updated state
      setFormData((prevData) => {
        const updatedData = { ...prevData, [e.target.name]: e.target.value };
        console.log('Updated form data:', updatedData);
        return updatedData;
      });
    };

    const handleSubmit = async (e) => {
      e.preventDefault();
      setLoading(true);
      console.log('Before SignUp Hit the API', formData);
      
      try {
        // Make a POST request to the sign-up endpoint
        axios.post('http://localhost:8000/signup/add', formData, {
          headers: {
            'X-CSRF-Token': formData.csrf_token,
          },
          withCredentials: true,
        });

        // Handle the response data (if needed)
        console.log('Signup successful::::::After Hit the API', formData);
      } catch (error) {
        setError(error);
        if (error.response) {
          // The request was made and the server responded with a status code
          // that falls out of the range of 2xx
          console.error('Error data:', error.response.data);
          console.error('Error status:', error.response.status);
          console.error('Error headers:', error.response.headers);
        } else if (error.request) {
          // The request was made but no response was received
          console.error('Error request:', error.request);
        } else {
          // Something happened in setting up the request that triggered an Error
          console.error('Error message:', error.message);
        }
        console.error('Error config:', error.config);
      }
       finally {
        setLoading(false);
      }
    };

    return (
      <Container maxWidth="sm">
        <div>
          <h1>Signup Form</h1>
          <form onSubmit={handleSubmit}>
            <TextField
              label="Name"
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              fullWidth
              margin="normal"
            />
            <TextField
              label="Email"
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              fullWidth
              margin="normal"
            />
            <TextField
              label="Password"
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              fullWidth
              margin="normal"
            />
            {/* <input type="hidden" name="csrf_token" value={formData.csrf_token} /> */}
            <Button type="submit" variant="contained" color="primary" disabled={loading} fullWidth>
              {loading ? 'Signing up...' : 'Sign Up'}
            </Button>
          </form>

          {error && <p>Error: {error.message}</p>}
        </div>
      </Container>
    );
  };

  export default SignupForm;