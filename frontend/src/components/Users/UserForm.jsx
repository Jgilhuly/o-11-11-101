import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { userApi } from '../../services/api'
import './UserForm.css'

export default function UserForm() {
  const navigate = useNavigate()
  const { userId } = useParams()
  const isEditing = !!userId

  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
  })
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (isEditing) {
      loadUser()
    }
  }, [userId])

  const loadUser = async () => {
    setLoading(true)
    try {
      const user = await userApi.getById(parseInt(userId))
      setFormData({
        name: user.name,
        email: user.email,
        password: '',
      })
    } catch (err) {
      setError(err.message || 'Failed to load user')
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)
    setLoading(true)

    try {
      if (isEditing) {
        const payload = { name: formData.name, email: formData.email }
        if (formData.password) {
          payload.password = formData.password
        }
        await userApi.update(parseInt(userId), payload)
      } else {
        await userApi.create(formData)
      }

      navigate('/users')
    } catch (err) {
      setError(err.message || 'Failed to save user')
    } finally {
      setLoading(false)
    }
  }

  if (loading && isEditing) {
    return <div className="loading">Loading user...</div>
  }

  return (
    <div className="user-form-container">
      <h1>{isEditing ? 'Edit User' : 'Create New User'}</h1>

      {error && <div className="error-message">{error}</div>}

      <form onSubmit={handleSubmit} className="user-form">
        <div className="form-group">
          <label htmlFor="name">Full Name *</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
            placeholder="Enter full name"
          />
        </div>

        <div className="form-group">
          <label htmlFor="email">Email *</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
            placeholder="Enter email address"
          />
        </div>

        <div className="form-group">
          <label htmlFor="password">
            Password {isEditing ? '(leave blank to keep current)' : '*'}
          </label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required={!isEditing}
            placeholder={isEditing ? 'Leave blank to keep current password' : 'Enter password'}
          />
        </div>

        <div className="form-actions">
          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading}
          >
            {loading ? 'Saving...' : isEditing ? 'Update User' : 'Create User'}
          </button>
          <button
            type="button"
            className="btn btn-secondary"
            onClick={() => navigate('/users')}
            disabled={loading}
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  )
}

