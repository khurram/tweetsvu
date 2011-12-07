require 'sinatra/base'

class MyApp < Sinatra::Base
  get '/' do
    erb :index
  end
end
