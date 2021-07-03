import React, { useState, useEffect, useReducer } from "react";
import { Row, Col, Container, Spinner } from "react-bootstrap";

import axios from "axios";

interface Schedule {
  stream_date: string;
  start_time: string;
  end_time: string;
  what: string;
  description?: string;
}

type State =
  | { loading: true }
  | { loading: false; error: string; schedules: null }
  | { loading: false; error: null; schedules: Schedule[] };

type Action =
  | { type: "loading" }
  | { type: "failure"; error: string }
  | { type: "success"; schedules: Schedule[] };

const defaultState: State = { loading: true };
/*const allSchedules: Schedule[] = [
  { date: "Mon 08th Mar", from: "", to: "", what: "NO STREAM" },
  { date: "Tue 09th Mar", from: "18:00", to: "23:30", what: "Hearthstone" },
  { date: "Wed 10th Mar", from: "19:00", to: "00:00", what: "Blasphemous" },
  {
    date: "Thu 11th Mar",
    from: "17:00",
    to: "23:30",
    what: "Hearthstone, Terraria",
  },
  { date: "Fri 12th Mar", from: "18:00", to: "00:00", what: "Blasphemous" },
  { date: "Sat 13th Mar", from: "18:00", to: "00:00", what: "Warcraft III" },
  { date: "Sun 14th Mar", from: "17:30", to: "23:30", what: "Trine 2" },
  {
    date: "Mon 15th Mar",
    from: "18:00",
    to: "23:30",
    what: "Legion TD 1v1s on ENT",
  },
  { date: "Tue 16th Mar", from: "18:00", to: "23:30", what: "Hearthstone" },
  { date: "Wed 17th Mar", from: "17:30", to: "00:00", what: "Blasphemous" },
];*/

const reducer = (state: State, action: Action): State => {
  switch (action.type) {
    case "loading":
      return { loading: true };
    case "failure":
      return { loading: false, error: action.error, schedules: null };
    case "success":
      return { loading: false, error: null, schedules: action.schedules };
  }
};

const AccurateSchedule = () => {
  const [state, dispatch] = useReducer(reducer, defaultState);

  useEffect(() => {
    axios
      .get("/api/v1/schedule/")
      .then((response) => {
        dispatch({ type: "success", schedules: response.data });
      })
      .catch((error) => {
        dispatch({ type: "failure", error: error.message });
      });
  }, []);

  const emptyFiller = (
    <>
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
    </>
  );

  if (state.loading === true) {
    return (
      <Container fluid className="justify-content-center">
        <Spinner animation="border" role="status" />
        &nbsp;&nbsp;Loading...
        {emptyFiller}
      </Container>
    );
  } else if (state.loading === false && state.schedules === null) {
    return (
      <Container fluid className="justify-content-center">
        ERROR: {state.error}
        {emptyFiller}
      </Container>
    );
  } else if (state.loading === false && state.error === null) {
    return (
      <Row className="justify-content-center">
        {state.schedules.splice(0, 12).map((schedule) => {
          return (
            <Col
              key={`${schedule.stream_date}${schedule.start_time}${schedule.end_time}`}
              xs={12}
              md={6}
              lg={4}
              className="text-center padding"
            >
              <h3>{schedule.stream_date}</h3>
              <h5>
                {schedule.start_time}-{schedule.end_time}
              </h5>
              <h2>{schedule.what}</h2>
            </Col>
          );
        })}
      </Row>
    );
  }

  throw Error("Wrong state!");
};

export default AccurateSchedule;
