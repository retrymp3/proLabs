require 'sinatra'
require 'yaml'

set :bind, '0.0.0.0'

# Sample user data
users = {
  "john" => {
    "name" => "John Doe",
    "email" => "john@example.com",
    "phone" => "555-555-1234"
  },
  "jane" => {
    "name" => "Jane Doe",
    "email" => "jane@example.com",
    "phone" => "555-555-5678"
  }
}

get '/' do
  erb :index
end

post '/submit' do
  code = params[:code]
  begin
    data = YAML.load(code)
    result = "No result"
    if data.is_a?(Hash)
      # Process the YAML data to change user details
      user = data["user"]
      if users.key?(user)
        users[user].merge!(data["details"])
        result = "User details updated: #{users[user].inspect}"
      else
        result = "User not found"
      end
    end
    erb :result, :locals => { :result => result }
  rescue => e
    erb :result, :locals => { :result => "Error: #{e.message}" }
  end
end