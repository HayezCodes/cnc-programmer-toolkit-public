import math


EPSILON = 1e-12


def included_angle_half_tangent(included_angle_deg: float) -> float:
    if included_angle_deg <= 0 or included_angle_deg >= 180:
        raise ValueError("Included angle must be greater than 0 and less than 180 degrees.")

    tangent_value = math.tan(math.radians(included_angle_deg / 2))
    if abs(tangent_value) < EPSILON:
        raise ValueError("Included angle creates an invalid chamfer calculation.")

    return tangent_value


def cone_depth_between_diameters(
    start_dia: float,
    target_dia: float,
    included_angle_deg: float,
) -> float:
    if target_dia <= start_dia:
        raise ValueError("Target diameter must be larger than the starting diameter.")

    return (target_dia - start_dia) / (2 * included_angle_half_tangent(included_angle_deg))


def center_drill_total_depth_for_target(
    pilot_dia: float,
    target_dia: float,
    included_angle_deg: float,
    tool_pilot_length_c: float,
) -> float:
    if tool_pilot_length_c < 0:
        raise ValueError("Tool Pilot Length / Full Depth Offset (C) must be zero or positive.")

    return tool_pilot_length_c + cone_depth_between_diameters(
        pilot_dia,
        target_dia,
        included_angle_deg,
    )


def center_drill_diameter_at_depth(
    pilot_dia: float,
    included_angle_deg: float,
    tool_pilot_length_c: float,
    total_depth: float,
) -> float:
    if tool_pilot_length_c < 0:
        raise ValueError("Tool Pilot Length / Full Depth Offset (C) must be zero or positive.")

    if total_depth < 0:
        raise ValueError("Total depth must be zero or positive.")

    tangent_value = included_angle_half_tangent(included_angle_deg)
    active_cone_depth = max(0.0, total_depth - tool_pilot_length_c)
    return pilot_dia + (2 * active_cone_depth * tangent_value)


def derive_center_drill_c_from_full_z(
    pilot_dia: float,
    full_target_dia: float,
    included_angle_deg: float,
    measured_full_depth: float,
) -> float:
    if measured_full_depth < 0:
        raise ValueError("Measured full depth must be zero or positive.")

    return measured_full_depth - cone_depth_between_diameters(
        pilot_dia,
        full_target_dia,
        included_angle_deg,
    )


def target_diameter_from_length_and_angle(
    existing_hole_dia: float,
    chamfer_edge_drop: float,
    chamfer_included_angle_deg: float,
    backoff_clearance_dia: float = 0.0,
) -> float:
    if existing_hole_dia <= 0:
        raise ValueError("Existing hole diameter must be greater than 0.")

    if chamfer_edge_drop <= 0:
        raise ValueError("Chamfer length / edge drop must be greater than 0.")

    if backoff_clearance_dia < 0:
        raise ValueError("Backoff / Clearance on Diameter must be zero or positive.")

    tangent_value = included_angle_half_tangent(chamfer_included_angle_deg)
    return existing_hole_dia + (2 * chamfer_edge_drop * tangent_value) - backoff_clearance_dia
