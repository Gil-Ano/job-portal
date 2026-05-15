import { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext";
import API from "../api";

export default function EmployerDashboard() {
  const { user } = useAuth();
  const [tab, setTab] = useState("my-jobs");
  const [jobs, setJobs] = useState([]);
  const [applications, setApplications] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [editJob, setEditJob] = useState(null);
  const [form, setForm] = useState({
    title: "",
    location: "",
    salary_min: "",
    salary_max: "",
    description: "",
    requirements: "",
    type: "full-time",
    category: "",
  });
  const [msg, setMsg] = useState("");

  useEffect(() => {
    fetchJobs();
    fetchApplications();
  }, []);

  const fetchJobs = async () => {
    const res = await API.get("/jobs");
    setJobs(res.data.filter((j) => j.employer_id && j.company));
  };

  const fetchApplications = async () => {
    try {
      const res = await API.get("/applications/received");
      setApplications(res.data);
    } catch (err) {
      console.error("Failed to load applications");
    }
  };

  const resetForm = () => {
    setForm({
      title: "",
      location: "",
      salary_min: "",
      salary_max: "",
      description: "",
      requirements: "",
      type: "full-time",
      category: "",
    });
    setEditJob(null);
    setShowForm(false);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMsg("");
    try {
      if (editJob) {
        await API.put(`/jobs/${editJob.id}`, form);
        setMsg("Job updated!");
      } else {
        await API.post("/jobs", form);
        setMsg("Job posted!");
      }
      resetForm();
      fetchJobs();
    } catch (err) {
      setMsg(err.response?.data?.detail || "Failed");
    }
  };

  const handleEdit = (job) => {
    setEditJob(job);
    setForm({
      title: job.title,
      location: job.location,
      salary_min: job.salary_min || "",
      salary_max: job.salary_max || "",
      description: job.description,
      requirements: job.requirements || "",
      type: job.type,
      category: job.category || "",
    });
    setShowForm(true);
  };

  const handleDelete = async (jobId) => {
    if (!confirm("Delete this job?")) return;
    await API.delete(`/jobs/${jobId}`);
    fetchJobs();
  };

  const handleStatus = async (appId, status) => {
    await API.put(`/applications/${appId}/status?status=${status}`);
    fetchApplications();
  };

  return (
    <div className="max-w-5xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-2">Employer Dashboard</h1>
      <p className="text-gray-500 mb-6">Welcome, {user?.full_name}</p>

      {/* Tabs */}
      <div className="flex gap-4 mb-6 border-b">
        {["my-jobs", "applications"].map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`pb-2 px-1 text-sm font-medium transition ${
              tab === t
                ? "text-green-600 border-b-2 border-green-600"
                : "text-gray-500"
            }`}
          >
            {t === "my-jobs"
              ? "My Jobs"
              : `Applications (${applications.length})`}
          </button>
        ))}
      </div>

      {/* My Jobs */}
      {tab === "my-jobs" && (
        <div>
          <button
            onClick={() => {
              resetForm();
              setShowForm(!showForm);
            }}
            className="bg-green-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-green-700 mb-4"
          >
            {showForm ? "Cancel" : "+ Post New Job"}
          </button>

          {msg && <p className="text-sm text-green-600 mb-3">{msg}</p>}

          {showForm && (
            <form
              onSubmit={handleSubmit}
              className="bg-white p-4 rounded-xl shadow-sm border mb-6 grid grid-cols-2 gap-3"
            >
              <input
                placeholder="Job Title"
                value={form.title}
                onChange={(e) => setForm({ ...form, title: e.target.value })}
                className="border rounded-lg px-3 py-2 text-sm"
                required
              />
              <input
                placeholder="Location"
                value={form.location}
                onChange={(e) => setForm({ ...form, location: e.target.value })}
                className="border rounded-lg px-3 py-2 text-sm"
                required
              />
              <input
                type="number"
                placeholder="Salary Min"
                value={form.salary_min}
                onChange={(e) =>
                  setForm({ ...form, salary_min: e.target.value })
                }
                className="border rounded-lg px-3 py-2 text-sm"
              />
              <input
                type="number"
                placeholder="Salary Max"
                value={form.salary_max}
                onChange={(e) =>
                  setForm({ ...form, salary_max: e.target.value })
                }
                className="border rounded-lg px-3 py-2 text-sm"
              />
              <select
                value={form.type}
                onChange={(e) => setForm({ ...form, type: e.target.value })}
                className="border rounded-lg px-3 py-2 text-sm"
              >
                <option value="full-time">Full-time</option>
                <option value="part-time">Part-time</option>
                <option value="contract">Contract</option>
                <option value="internship">Internship</option>
              </select>
              <input
                placeholder="Category"
                value={form.category}
                onChange={(e) => setForm({ ...form, category: e.target.value })}
                className="border rounded-lg px-3 py-2 text-sm"
              />
              <textarea
                placeholder="Description"
                value={form.description}
                onChange={(e) =>
                  setForm({ ...form, description: e.target.value })
                }
                className="border rounded-lg px-3 py-2 text-sm col-span-2"
                rows={3}
                required
              />
              <textarea
                placeholder="Requirements"
                value={form.requirements}
                onChange={(e) =>
                  setForm({ ...form, requirements: e.target.value })
                }
                className="border rounded-lg px-3 py-2 text-sm col-span-2"
                rows={2}
              />
              <button
                type="submit"
                className="col-span-2 bg-green-600 text-white py-2 rounded-lg font-medium hover:bg-green-700"
              >
                {editJob ? "Update Job" : "Post Job"}
              </button>
            </form>
          )}

          <div className="space-y-3">
            {jobs.map((job) => (
              <div
                key={job.id}
                className="bg-white p-4 rounded-xl shadow-sm border flex justify-between items-center"
              >
                <div>
                  <h3 className="font-semibold">{job.title}</h3>
                  <p className="text-sm text-gray-500">
                    {job.location} · {job.type} · ${job.salary_min}
                  </p>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => handleEdit(job)}
                    className="text-xs bg-gray-100 px-3 py-1 rounded-lg hover:bg-gray-200"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => handleDelete(job.id)}
                    className="text-xs bg-red-50 text-red-600 px-3 py-1 rounded-lg hover:bg-red-100"
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Applications */}
      {tab === "applications" && (
        <div className="space-y-4">
          {applications.length === 0 ? (
            <p className="text-gray-500 text-sm">
              No applications received yet.
            </p>
          ) : (
            applications.map((app) => (
              <div
                key={app.id}
                className="bg-white p-4 rounded-xl shadow-sm border"
              >
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="font-semibold">{app.applicant_name}</h3>
                    <p className="text-sm text-gray-500">
                      {app.applicant_email}
                    </p>
                    <p className="text-sm text-gray-600 mt-1">
                      For: {app.job_title}
                    </p>
                    {app.match_score !== null && (
                      <span className="text-xs text-green-600 font-medium">
                        {app.match_score}% match
                      </span>
                    )}
                    {app.cover_letter && (
                      <p className="text-sm text-gray-500 mt-1 italic">
                        "{app.cover_letter}"
                      </p>
                    )}
                  </div>
                  <div className="text-right">
                    <span
                      className={`text-xs px-2 py-1 rounded-full font-medium ${
                        app.status === "applied"
                          ? "bg-yellow-100 text-yellow-700"
                          : app.status === "accepted"
                            ? "bg-green-100 text-green-700"
                            : "bg-gray-100 text-gray-700"
                      }`}
                    >
                      {app.status}
                    </span>
                    <div className="flex gap-1 mt-2">
                      <button
                        onClick={() => handleStatus(app.id, "reviewed")}
                        className="text-xs bg-blue-50 text-blue-600 px-2 py-1 rounded"
                      >
                        Review
                      </button>
                      <button
                        onClick={() => handleStatus(app.id, "shortlisted")}
                        className="text-xs bg-purple-50 text-purple-600 px-2 py-1 rounded"
                      >
                        Shortlist
                      </button>
                      <button
                        onClick={() => handleStatus(app.id, "accepted")}
                        className="text-xs bg-green-50 text-green-600 px-2 py-1 rounded"
                      >
                        Accept
                      </button>
                      <button
                        onClick={() => handleStatus(app.id, "rejected")}
                        className="text-xs bg-red-50 text-red-600 px-2 py-1 rounded"
                      >
                        Reject
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}
