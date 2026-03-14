export interface User {
  id: string;
  email: string;
  name?: string;
  created_at: string;
}

export interface FlightPreference {
  user_id: string;
  loyalty_program?: string;
  seat_preference?: string;
  alliance?: string;
  max_connections: number;
}

export interface MonitoredFlight {
  id: string;
  user_id: string;
  flight_no: string;
  icao24?: string;
  dep_airport: string;
  arr_airport: string;
  scheduled_dep: string;
  status: 'SCHEDULED' | 'DELAYED' | 'CANCELLED' | 'LANDED';
  created_at: string;
}

export interface Disruption {
  id: string;
  flight_id: string;
  type: 'DELAY' | 'CANCEL' | 'DIVERT';
  delay_minutes?: number;
  cause?: string;
  detected_at: string;
}

export interface Claim {
  id: string;
  disruption_id?: string;
  user_id: string;
  carrier: string;
  regulation: 'EC261' | 'UK261' | 'DOT';
  amount_eur?: number;
  status: 'DRAFT' | 'SUBMITTED' | 'ACCEPTED' | 'REJECTED' | 'APPEALED' | 'PAID';
  submitted_at?: string;
  resolved_at?: string;
}

export interface DisruptionAlert {
  flight_id: string;
  flight_no: string;
  type: 'DELAY' | 'CANCEL' | 'DIVERT';
  delay_minutes: number;
  rebook_options?: ReBookOption[];
}

export interface ReBookOption {
  flight_no: string;
  carrier: string;
  dep_time: string;
  arr_time: string;
  stops: number;
  duration_min: number;
}
