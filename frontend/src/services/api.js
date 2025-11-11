const API_BASE_URL = 'http://localhost:8000';

// Helper function to handle responses
async function handleResponse(response) {
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'An error occurred');
  }
  return response.json();
}

// PRODUCTS API CALLS
export const productApi = {
  // Get all products
  getAll: async () => {
    const response = await fetch(`${API_BASE_URL}/products`);
    return handleResponse(response);
  },

  // Get a specific product by ID
  getById: async (id) => {
    const response = await fetch(`${API_BASE_URL}/products/${id}`);
    return handleResponse(response);
  },

  // Create a new product
  create: async (productData) => {
    const response = await fetch(`${API_BASE_URL}/products`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(productData),
    });
    return handleResponse(response);
  },

  // Update an existing product
  update: async (id, productData) => {
    const response = await fetch(`${API_BASE_URL}/products/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(productData),
    });
    return handleResponse(response);
  },

  // Delete a product
  delete: async (id) => {
    const response = await fetch(`${API_BASE_URL}/products/${id}`, {
      method: 'DELETE',
    });
    return handleResponse(response);
  },
};

// USERS API CALLS
export const userApi = {
  // Get all users
  getAll: async () => {
    const response = await fetch(`${API_BASE_URL}/users`);
    return handleResponse(response);
  },

  // Get a specific user by ID
  getById: async (id) => {
    const response = await fetch(`${API_BASE_URL}/users/${id}`);
    return handleResponse(response);
  },

  // Create a new user
  create: async (userData) => {
    const response = await fetch(`${API_BASE_URL}/users`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    });
    return handleResponse(response);
  },

  // Update an existing user
  update: async (id, userData) => {
    const response = await fetch(`${API_BASE_URL}/users/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    });
    return handleResponse(response);
  },

  // Delete a user
  delete: async (id) => {
    const response = await fetch(`${API_BASE_URL}/users/${id}`, {
      method: 'DELETE',
    });
    return handleResponse(response);
  },
};

