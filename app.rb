require 'sinatra/base'
require 'twitter'

class MyApp < Sinatra::Base
  get '/' do
    erb :index
  end
  
  post '/search' do
    @query = params[:query]
    @results = Twitter.search(@query)
    erb :index
  end

  get '/report' do
    erb :report
  end
end
