import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { userApi } from '../../services/api'
import UserCard from './UserCard'
import './UserList.css'

export default function UserList() {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchUsers()
  }, [])

  const fetchUsers = async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await userApi.getAll()
      setUsers(data)
    } catch (err) {
      setError(err.message || 'Failed to fetch users')
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id) => {
    try {
      await userApi.delete(id)
      setUsers(users.filter((u) => u.id !== id))
    } catch (err) {
      setError(err.message || 'Failed to delete user')
    }
  }

  if (loading) {
    return <div className="loading">Loading users...</div>
  }

  return (
    <div className="user-list-container">
      <div className="user-list-header">
        <h1>Users</h1>
        <Link to="/users/new" className="btn btn-primary">
          Add New User
        </Link>
      </div>

      {error && <div className="error-message">{error}</div>}

      {users.length === 0 ? (
        <div className="empty-state">
          <p>No users found. Create one to get started!</p>
          <Link to="/users/new" className="btn btn-primary">
            Create First User
          </Link>
        </div>
      ) : (
        <div className="users-grid">
          {users.map((user) => (
            <UserCard
              key={user.id}
              user={user}
              onDelete={handleDelete}
            />
          ))}
        </div>
      )}
    </div>
  )
}

