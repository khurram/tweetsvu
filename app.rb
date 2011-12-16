require 'sinatra/base'
require 'twitter'
require 'twitter-text'

class App < Sinatra::Base
  include Twitter::Autolink
  
  get '/' do
    erb :index
  end
  
  get '/search' do
    @query = params[:q]
    @results = Twitter.search(@query, :rpp => 100, :include_entities => true)
    erb :index
  end

  get '/report' do
    erb :report
  end
end
