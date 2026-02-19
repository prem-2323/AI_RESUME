from pydantic import BaseModel

class RoleRequest(BaseModel):
    role: str

class JDRequest(BaseModel):
    job_description: str

class CompanyRoleRequest(BaseModel):
    company_name: str
    job_role: str

class CareerSwitchRequest(BaseModel):
    current_role: str
    target_role: str
