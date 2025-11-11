import { Link } from 'react-router-dom'
import './UserCard.css'

export default function UserCard({ user, onDelete }) {
  const handleDelete = () => {
    if (window.confirm(`Are you sure you want to delete the user "${user.name}"?`)) {
      onDelete(user.id)
    }
  }

  return (
    <div className="user-card">
      <div className="user-header">
        <div className="user-avatar">{user.name.charAt(0).toUpperCase()}</div>
        <div className="user-info">
          <h3>{user.name}</h3>
          <p className="user-email">{user.email}</p>
        </div>
      </div>
      <div className="user-actions">
        <Link to={`/users/${user.id}/edit`} className="btn btn-primary">
          Edit
        </Link>
        <button onClick={handleDelete} className="btn btn-danger">
          Delete
        </button>
      </div>
    </div>
  )
}

