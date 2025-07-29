import os
from mcp.server.fastmcp import FastMCP

# Create the MCP server
mcp = FastMCP("os_tool_server", 
              instructions="You are an OS operations assistant that can perform file system operations.",
              port=8003)


@mcp.tool()
def get_absolute_path(folder_name: str = None, file_name: str = None) -> list:
    """
    Searches for all directories with the specified folder name within the
    "/Users/L036202/Desktop/" directory tree, excluding certain system and hidden folders.
    
    Args:
    
        folder_name (str): The name of the folder to search for.
        
    Returns:
        list: A list of absolute paths to directories matching the folder_name.
        
    Notes:
        - Excludes directories named '.env', '.venv', '__pycache__', and any directories
          starting with '.' or '_'.
        - Searches recursively through the entire Desktop directory tree.
    """
    try: 
        print("get_absolute_path tool triggred")
        print("params for get_absolute_path are: ", folder_name, file_name)
        if folder_name:
            print("folder condition triggered")
            list_of_folder_paths = []
            found_dirs = False
            for root, dirs, files in os.walk("/Users/L036202/Desktop/test_folder_mcp"):
                dirs[:]= [d for d in dirs if d not in {'.env', '.venv', '__pycache__'} and not d.startswith(('.', '_'))]
                for d in dirs:
                    if d == folder_name:
                        print(f"FOUND MATCH: {d} in {root}")
                        found_dirs = True
                        list_of_folder_paths.append(os.path.join(root, d))
            if found_dirs:
                return list_of_folder_paths
            else:
                return {"message": "Sorry, could not find the folder on Desktop/test_folder_mcp, try a different name"}
                        
        elif file_name:
            print("file name triggered")
            list_of_file_paths = []
            found_file = False
            for root, dirs, files in os.walk("/Users/L036202/Desktop/test_folder_mcp"):
                dirs[:]= [d for d in dirs if d not in {'.env', '.venv', '__pycache__'} and not d.startswith(('.', '_'))]
                for file in files:

                    print("any file is:", file)
                    if file.endswith('.txt'):
                        print("only text file is :", file)
                        if file == file_name:
                            found_file = True
                            list_of_file_paths.append(os.path.join(root, file))
            if found_file:                
                return list_of_file_paths
            
            else:
                return {"message": "Sorry, could not find the file_name on Desktop/test_folder_mcp, try a different name"}
                                
        else:
            return {"message":"I didnt understand the input, I accept folder_name: name of the folder and file_name: name of the file name and will return the absolute path of the given folder name and the file name"}
    
    except Exception as e:
        return {"error_message": f"Internal procession error and the error is: {e}"}   

@mcp.tool()
def list_directory_contents(list_of_folder_paths: list) -> dict:
    """List all files and folders from multiple directory paths.
    
    Args:
        list_of_folder_paths (list): A list of directory paths to scan for files and folders.
        
    Returns:
        dict: A dictionary containing 'folders' and 'files' keys with lists of found items.
              - 'folders': List of all subdirectories found in the provided paths
              - 'files': List of all files found in the provided paths (excluding hidden files)
              
    Notes:
        - Hidden files (starting with '.') are excluded from the results
        - The function recursively walks through all provided directory paths
    """
    all_files = []
    all_folders = []
    print("list_directory_contents")
    print("params for get_absolute_path are: ", list_of_folder_paths)
    for folder_path in list_of_folder_paths:
        try:
            for root, dirs, files in os.walk(folder_path):
                # Add directories to the folders list
                for d in dirs:
                    print("folder is ", d)
                    if not d.startswith('.'):
                        all_folders.append(os.path.join(root, d))
                
                # Add files to the files list (excluding hidden files)
                for f in files:
                    print("the files are", f)
                    if not f.startswith('.'):
                        all_files.append(os.path.join(root, f))
            result = {folder_path:{'folders': all_folders, 'files': all_files} }
        except (PermissionError, FileNotFoundError) as e:
            print(f"Warning: Could not access {folder_path}: {e}")
            continue
    
    return result



@mcp.tool()
def get_file_info(file_path: str) -> dict:
    """
    Retrieves content information from a file.
    
    Args:
        file_path (str): The path to the file from which to extract content.
                        If empty or None, an error will be returned.
    
    Returns:
        dict: A dictionary containing 'content': The extracted text content from the file

              
    """
    print("get_file_info tool triggered")
    print("params for get_file_info are", file_path)
    if file_path:
        content = ('The pursuit of happiness can sometimes seem like a difficult thing. '
                  'Contentment, peace, and satisfaction can elude us all too well. '
                  'In times like these, mental and emotional well-being are more important than ever. '
                  'They are the cornerstones of a healthy and fulfilling life. '
                  'In this article, we\'ll take a closer look at mental and emotional health '
                  'and provide actionable ways to promote wellness in our daily lives.')
        return {'content': content}
    else:
        return {'error': 'File path not given, need file path for getting the content'}




#the below is a mock tool for demo purposes
@mcp.tool()
def get_summary_of_file(file_content: str) -> dict:
    """
    Generates a summary of the provided file content.
    
    Args:
        file_content (str): The text content to be summarized.
                           If empty or None, an error will be returned.
    
    Returns:
        dict: A dictionary containing 'summary': A condensed version of the input content highlighting key points

    """
    if file_content:
        summary = ('The journey toward happiness can be challenging, with peace and contentment '
                  'often feeling out of reach. In such times, prioritizing mental and emotional '
                  'well-being becomes essential, as they form the foundation of a healthy and '
                  'fulfilling life. This article explores the importance of mental and emotional '
                  'health and offers practical strategies to enhance wellness in everyday life.')
        return {'summary': summary}
    else:
        return {'error': 'file_content was not given to this function'}

@mcp.tool()
def test():
    return


if __name__ == "__main__":
    # Start the MCP server with SSE transport
    mcp.run(transport="sse")
