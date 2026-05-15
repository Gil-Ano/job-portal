import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import API from "../api";

export default function JobDetail() {
  const { id } = useParams();
  const { user } = useAuth();
  const navigate = useNavigate();
  const [job, setJob] = useState(null);
  const [loading, setLoading] = useState(true);
  const [applying, setApplying] = useState(false);
  const [coverLetter, setCoverLetter] = useState("");
  const [message, setMessage] = useState("");
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    fetchJob();
  }, [id]);

  const fetchJob = async () => {
    try {
      const res = await API.get(`/jobs/${id}`);
      setJob(res.data);
    } catch (err) {
      console.error("Job not found");
    }
    setLoading(false);
  };

  const handleApply = async () => {
    if (!user) {
      navigate("/login");
      return;
    }
    setApplying(true);
    setMessage("");
    try {
      await API.post("/applications", {
        job_id: parseInt(id),
        cover_letter: coverLetter,
      });
      setMessage("Application submitted successfully!");
    } catch (err) {
      setMessage(err.response?.data?.detail || "Failed to apply");
    }
    setApplying(false);
  };

  const handleSave = async () => {
    if (!user) return navigate("/login");
    try {
      if (saved) {
        await API.delete(`/jobs/${id}/save`);
        setSaved(false);
      } else {
        await API.post(`/jobs/${id}/save`);
        setSaved(true);
      }
    } catch (err) {
      console.error("Save failed");
    }
  };

  if (loading)
    return (
      <div className="max-w-3xl mx-auto p-6">
        <p className="text-gray-500">Loading...</p>
      </div>
    );
  if (!job)
    return (
      <div className="max-w-3xl mx-auto p-6">
        <p className="text-gray-500">Job not found.</p>
      </div>
    );

  return (
    <div className="max-w-3xl mx-auto p-6">
      <div className="bg-white p-6 rounded-xl shadow-sm border">
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-2xl font-bold text-gray-800">{job.title}</h1>
            <p className="text-gray-600">
              {job.company} — {job.location}
            </p>
          </div>
          <span className="bg-green-100 text-green-700 text-sm font-medium px-3 py-1 rounded-full">
            {job.type}
          </span>
        </div>

        {job.salary_min && (
          <p className="text-lg font-semibold text-green-600 mt-4">
            ${job.salary_min} - ${job.salary_max}
          </p>
        )}

        <div className="mt-6">
          <h2 className="text-lg font-semibold mb-2">Description</h2>
          <p className="text-gray-700 whitespace-pre-wrap">{job.description}</p>
        </div>

        {job.requirements && (
          <div className="mt-6">
            <h2 className="text-lg font-semibold mb-2">Requirements</h2>
            <p className="text-gray-700 whitespace-pre-wrap">
              {job.requirements}
            </p>
          </div>
        )}

        <div className="flex gap-3 mt-6 text-sm text-gray-500">
          {job.category && (
            <span className="bg-gray-100 px-3 py-1 rounded-full">
              {job.category}
            </span>
          )}
          <span>Posted: {new Date(job.created_at).toLocaleDateString()}</span>
        </div>

        {/* Actions */}
        <div className="mt-8 border-t pt-6">
          {user?.role === "jobseeker" ? (
            <div className="space-y-4">
              <textarea
                value={coverLetter}
                onChange={(e) => setCoverLetter(e.target.value)}
                placeholder="Write a short cover letter (optional)..."
                className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none"
                rows={3}
              />
              <div className="flex gap-3">
                <button
                  onClick={handleApply}
                  disabled={applying}
                  className="bg-green-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-green-700 transition disabled:opacity-50"
                >
                  {applying ? "Submitting..." : "Apply Now"}
                </button>
                <button
                  onClick={handleSave}
                  className={`px-6 py-2 rounded-lg font-medium border transition ${
                    saved
                      ? "bg-green-50 text-green-700 border-green-300"
                      : "bg-white text-gray-700 border-gray-300 hover:bg-gray-50"
                  }`}
                >
                  {saved ? "❤️ Saved" : "🤍 Save Job"}
                </button>
              </div>
              {message && (
                <p
                  className={`text-sm ${message.includes("success") ? "text-green-600" : "text-red-600"}`}
                >
                  {message}
                </p>
              )}
            </div>
          ) : user?.role === "employer" ? (
            <p className="text-gray-500 text-sm">
              Employers cannot apply to jobs.
            </p>
          ) : (
            <p className="text-gray-500 text-sm">
              <button
                onClick={() => navigate("/login")}
                className="text-green-600 hover:underline font-medium"
              >
                Login
              </button>{" "}
              as a jobseeker to apply.
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
