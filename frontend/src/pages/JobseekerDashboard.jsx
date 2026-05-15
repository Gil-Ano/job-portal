import { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext";
import API from "../api";

export default function JobseekerDashboard() {
  const { user } = useAuth();
  const [applications, setApplications] = useState([]);
  const [savedJobs, setSavedJobs] = useState([]);
  const [tab, setTab] = useState("applications");
  const [uploadMsg, setUploadMsg] = useState("");
  const [cvFile, setCvFile] = useState(null);

  useEffect(() => {
    fetchApplications();
    fetchSavedJobs();
  }, []);

  const fetchApplications = async () => {
    try {
      const res = await API.get("/applications/my");
      setApplications(res.data);
    } catch (err) {
      console.error("Failed to load applications");
    }
  };

  const fetchSavedJobs = async () => {
    try {
      const res = await API.get("/jobs/saved/mine");
      setSavedJobs(res.data);
    } catch (err) {
      console.error("Failed to load saved jobs");
    }
  };

  const handleCVUpload = async (e) => {
    e.preventDefault();
    if (!cvFile) return;
    const formData = new FormData();
    formData.append("file", cvFile);

    try {
      const res = await API.post("/applications/upload-cv", formData);
      setUploadMsg(res.data.message);
    } catch (err) {
      setUploadMsg(err.response?.data?.detail || "Upload failed");
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      applied: "bg-yellow-100 text-yellow-700",
      reviewed: "bg-blue-100 text-blue-700",
      shortlisted: "bg-purple-100 text-purple-700",
      accepted: "bg-green-100 text-green-700",
      rejected: "bg-red-100 text-red-700",
    };
    return colors[status] || "bg-gray-100 text-gray-700";
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-2">My Dashboard</h1>
      <p className="text-gray-500 mb-6">Welcome, {user?.full_name}</p>

      {/* Tabs */}
      <div className="flex gap-4 mb-6 border-b">
        <button
          onClick={() => setTab("applications")}
          className={`pb-2 px-1 text-sm font-medium transition ${
            tab === "applications"
              ? "text-green-600 border-b-2 border-green-600"
              : "text-gray-500 hover:text-gray-700"
          }`}
        >
          My Applications ({applications.length})
        </button>
        <button
          onClick={() => setTab("saved")}
          className={`pb-2 px-1 text-sm font-medium transition ${
            tab === "saved"
              ? "text-green-600 border-b-2 border-green-600"
              : "text-gray-500 hover:text-gray-700"
          }`}
        >
          Saved Jobs ({savedJobs.length})
        </button>
        <button
          onClick={() => setTab("cv")}
          className={`pb-2 px-1 text-sm font-medium transition ${
            tab === "cv"
              ? "text-green-600 border-b-2 border-green-600"
              : "text-gray-500 hover:text-gray-700"
          }`}
        >
          Upload CV
        </button>
      </div>

      {/* Applications Tab */}
      {tab === "applications" && (
        <div className="space-y-4">
          {applications.length === 0 ? (
            <p className="text-gray-500 text-sm">No applications yet.</p>
          ) : (
            applications.map((app) => (
              <div
                key={app.id}
                className="bg-white p-4 rounded-xl shadow-sm border"
              >
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="font-semibold text-gray-800">
                      {app.job_title}
                    </h3>
                    <p className="text-sm text-gray-500">{app.company}</p>
                  </div>
                  <span
                    className={`text-xs px-2 py-1 rounded-full font-medium ${getStatusColor(app.status)}`}
                  >
                    {app.status}
                  </span>
                </div>
                {app.match_score !== null && (
                  <div className="mt-2">
                    <div className="flex items-center gap-2">
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-green-500 h-2 rounded-full"
                          style={{ width: `${app.match_score}%` }}
                        />
                      </div>
                      <span className="text-sm font-medium text-gray-600">
                        {app.match_score}%
                      </span>
                    </div>
                    <p className="text-xs text-gray-400 mt-1">AI Match Score</p>
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      )}

      {/* Saved Jobs Tab */}
      {tab === "saved" && (
        <div className="space-y-4">
          {savedJobs.length === 0 ? (
            <p className="text-gray-500 text-sm">No saved jobs yet.</p>
          ) : (
            savedJobs.map((job) => (
              <div
                key={job.id}
                className="bg-white p-4 rounded-xl shadow-sm border"
              >
                <h3 className="font-semibold text-gray-800">{job.title}</h3>
                <p className="text-sm text-gray-500">
                  {job.company} — {job.location}
                </p>
                <p className="text-sm text-green-600 font-medium">
                  ${job.salary_min} - ${job.salary_max}
                </p>
              </div>
            ))
          )}
        </div>
      )}

      {/* CV Upload Tab */}
      {tab === "cv" && (
        <div className="bg-white p-6 rounded-xl shadow-sm border">
          <h3 className="font-semibold text-lg mb-4">Upload Your CV</h3>
          <form onSubmit={handleCVUpload} className="space-y-4">
            <input
              type="file"
              accept=".pdf"
              onChange={(e) => setCvFile(e.target.files[0])}
              className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-green-50 file:text-green-700 hover:file:bg-green-100"
            />
            <button
              type="submit"
              disabled={!cvFile}
              className="bg-green-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-green-700 transition disabled:opacity-50"
            >
              Upload CV
            </button>
          </form>
          {uploadMsg && (
            <p
              className={`mt-4 text-sm ${uploadMsg.includes("success") ? "text-green-600" : "text-red-600"}`}
            >
              {uploadMsg}
            </p>
          )}
          <p className="text-xs text-gray-400 mt-4">
            Upload your CV to get AI-powered match scores when you apply to
            jobs.
          </p>
        </div>
      )}
    </div>
  );
}
