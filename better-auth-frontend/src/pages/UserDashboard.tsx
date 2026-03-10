import { useGetUser } from "../hooks/useGetUser";

const UserDashboard = () => {
  const user = useGetUser();

  return (
    <div>
      <h1>Welcome {user?.username}</h1>
    </div>
  );
};

export default UserDashboard;
