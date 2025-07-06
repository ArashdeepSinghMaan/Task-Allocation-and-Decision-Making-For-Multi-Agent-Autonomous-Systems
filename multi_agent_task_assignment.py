import numpy as np

class Agent:
    def __init__(self, name, position, velocity=0, capability=0):
        self.name=name
        self.position=np.array(position)
        self.velocity=velocity
        self.capability=capability


class Tasks:
    def __init__(self, position, agent_name=""):
        self.position=np.array(position)
        

n_agents=3
n_tasks=5

A1=Agent["A1",(0,0,0)]
A2=Agent["A2",(4,0,0)]
A3=Agent["A3",(10,0,0)]
agents=[A1,A2,A3]
        
T1=Tasks["T1",(40,50,0)]
T2=Tasks["T2",(100,60,0)]
T3=Tasks["T3",(86,90,0)]
T4=Tasks["T4",(48,75,0)]
T5=Tasks["T5",(82,91,0)]
GCS=Tasks["GCS",(0,0,0)]

tasks=[1,T2,T3,T4,T5,GCS]

def capability_evaluation(agents, tasks):
    capability=np.zeros(n_agents,n_tasks)
    for j in range(n_tasks):
        for i in range(n_agents):
            capability[i][j]=np.linalg.norm(agents[i].position-tasks[j].position)

    return capability

def task_allocation(agents, tasks):
    capability=capability_evaluation(agents, tasks)
    for j in range(n_tasks):
        max=np.max(capability[:,j])
        for i in range(n_agents):
         capability[i][j]-=max

         if capability[i][j]>=0 :
             tasks[j].agent_name=agents[i].name
         elif capability[i][j]==np.inf :
             del tasks[j]
             GCS.agent_name=agents[i].name
    return tasks, capability

# Input communication relay time tables and assign them to the communication network
communication_network=np.zeros(n_agents,n_agents)

def permissible_communication_network(agents):
    permissible_communication_network=np.zeros(n_agents,n_agents)
    acceptable_factor=1.5
    for i in range(n_agents):
        for j in range(n_agents):
            permissible_communication_network[i][j]= acceptable_factor*(np.linalg.norm(agents[i].position-agents[j].position))
    return permissible_communication_network


def event_triggered_reassignment(communication_network,agents,tasks):
    permissible_communication_network=permissible_communication_network(agents)
    communication_error_matrix=communication_network-permissible_communication_network
    link_matrix=np.zeros(n_agents,n_agents)
    link_score_vector=np.zeros(1,n_agents)
    for j in range(n_agents):
        for i in range(n_agents):
            if communication_error_matrix[i][j]<=0 :
                link_matrix[i][j]=1
            else :
                link_matrix[i][j]=0
            link_score_vector[j]+=link_matrix[i][j]
        if link_score_vector[j]==0:
            del agents[j]
            for k in range(n_tasks):
                if tasks[k].name_agent==agents[j].name :
                    tasks[k].name_agent=""
            revised_capability=capability_evaluation(agents, tasks)
            updated_tasks, updated_capability=task_allocation(agents, tasks,updated_capability)
    return updated_tasks,updated_capability

        
       
    
               



    
        



             
             



    





