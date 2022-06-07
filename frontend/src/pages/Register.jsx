import { useState } from "react";
import { Button, Container, Form, FloatingLabel } from "react-bootstrap";
import "./Register.css";

const Register = () => {
  const [form, setForm] = useState({});
  const [errors, setErrors] = useState({});
  var currentAccess = localStorage.getItem("currentAccess");

  const setField = (field, value) => {
    setForm({
      ...form,
      [field]: value,
    });

    if (!!errors[field])
      setErrors({
        ...errors,
        [field]: null,
      });
  };

  const validateForm = () => {
    const { name, email, password, confirm_pass, faculty_id } = form;

    const newErrors = {};
    const id_format = /\d{4}-\d{5}/g;
    const regex =
      /^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;

    if (!name || name === "") newErrors.name = "Please enter your name!";
    if (!faculty_id || faculty_id === "")
      newErrors.faculty_id = "Please enter ID!";
    else if (id_fromat.test(faculty_id) === false) {
      newErrors.faculty_id =
        "Please enter your ID in this format: (XXXX-XXXXX)!";
    }
    if (!email || email === "")
      newErrors.email = "Please enter your email address!";
    else if (regex.test(email) === false) {
      newErrors.email =
        "Please enter your email address in this format: yourname@up.edu.ph";
    }

    if (!password || password === "")
      newErrors.password = "Please enter your password!";
    if (!confirm_pass || confirm_pass === "")
      newErrors.confirm_pass = "Please confirm your password!";
    else if (password !== confirm_pass) {
      newErrors.confirm_pass = "Passwords don't match!";
    }
    return newErrors;
  };

  const submitFormHandler = async (event) => {
    event.preventDefault();
    var access = access_level.value === "admin" ? 0 : 1;
    const { department, access_level } = event.target;
    const formErrors = validateForm();

    if (Object.keys(formErrors).length === 0) {
      const response = await fetch("/api/users", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
        },
        body: JSON.stringify({
          faculty_id: form.faculty_id,
          name: form.name,
          email: form.email,
          password: form.password,
          department: department.value,
          access_level: access,
        }),
      });

      switch (response.status) {
        case 300:
          location.reload();
          break;
        default:
          console.log("error");
      }
    }
    setErrors(formErrors);
  };

  return (
    <>
      {currentAccess == 0 && (
        <div fluid className="background">
          <div className="leftSide"></div>
          <div className="rightSide">
            <h1 className="text-center">Add Account</h1>
            <Container className="contain" fluid="xs">
              <Form onSubmit={submitFormHandler}>
                <FloatingLabel label="Full Name" className="mb-3 text-black">
                  <Form.Control
                    placeholder=" "
                    name="name"
                    value={form.name}
                    onChange={(e) => setField("name", e.target.value)}
                    isInvalid={!!errors.name}
                  />
                  <Form.Control.Feedback type="invalid">
                    {errors.name}
                  </Form.Control.Feedback>
                  {/* placeholder is set to any non-empty string for FloatingLabel to work */}
                </FloatingLabel>

                <FloatingLabel label="Faculty ID" className="mb-3 text-black">
                  <Form.Control
                    placeholder=" "
                    name="faculty_id"
                    pattern="\d{4}-\d{5}"
                    value={form.faculty_id}
                    onChange={(e) => setField("faculty_id", e.target.value)}
                    isInvalid={!!errors.faculty_id}
                  />
                  <Form.Control.Feedback type="invalid">
                    {errors.faculty_id}
                  </Form.Control.Feedback>
                </FloatingLabel>

                <FloatingLabel
                  label="Email address"
                  className="mb-3 text-black"
                >
                  <Form.Control
                    placeholder=" "
                    name="email"
                    value={form.email}
                    onChange={(e) => setField("email", e.target.value)}
                    isInvalid={!!errors.email}
                  />
                  <Form.Control.Feedback type="invalid">
                    {errors.email}
                  </Form.Control.Feedback>
                </FloatingLabel>

                <FloatingLabel label="Department" className="mb-3 text-black">
                  <Form.Select name="department" required>
                    <option value="IBS">
                      Institute of Biological Sciences (IBS)
                    </option>
                    <option value="IC">Institute of Chemistry (IC)</option>
                    <option>Institute of Computer Science (ICS)</option>
                    <option value="IMSP">
                      Institute of Mathematical Sciences and Physics (IMSP)
                    </option>
                    <option value="INSTAT">
                      Institute of Statistics (INSTAT)
                    </option>
                    <option value="DHUM">
                      Department of Humanities (DHUM)
                    </option>
                    <option value="DSS">
                      Department of Social Sciences (DSS)
                    </option>
                    <option value="DHK">
                      Department of Human Kinetics (DHK)
                    </option>
                    <option value="UPRHS">UP Rural High School (UPRHS)</option>
                  </Form.Select>
                </FloatingLabel>

                <FloatingLabel label="Access Level" className="mb-3 text-black">
                  <Form.Select name="access_level" required>
                    <option>Staff</option>
                    <option>Admin</option>
                  </Form.Select>
                </FloatingLabel>

                <FloatingLabel label="Password" className="mb-3 text-black">
                  <Form.Control
                    type="password"
                    placeholder=" "
                    name="password"
                    value={form.password}
                    onChange={(e) => setField("password", e.target.value)}
                    isInvalid={!!errors.password}
                  />
                  <Form.Control.Feedback type="invalid">
                    {errors.password}
                  </Form.Control.Feedback>
                </FloatingLabel>

                <FloatingLabel
                  label="Confirm Password"
                  className="mb-3 text-black"
                >
                  <Form.Control
                    type="password"
                    placeholder=" "
                    name="confirm_pass"
                    value={form.confirm_pass}
                    onChange={(e) => setField("confirm_pass", e.target.value)}
                    isInvalid={!!errors.confirm_pass}
                  />
                  <Form.Control.Feedback type="invalid">
                    {errors.confirm_pass}
                  </Form.Control.Feedback>
                </FloatingLabel>

                <Button type="submit">Save</Button>

                <a href="/settings">
                  <Button className="mx-3">Cancel</Button>
                </a>
              </Form>
            </Container>
          </div>
        </div>
      )}
    </>
  );
};

export default Register;
